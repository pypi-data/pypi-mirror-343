#!/usr/bin/python3
ver="2024-11-25"
############################################################
# X4XREF Ver. 2024-11-25
# (Utility for getting CrossRef metadata from reference code.)
#
# Naohiko Otuka (IAEA Nuclear Data Section)
#  on behalf of the International Network of
#  Nuclear Reaction Data Centres (NRDC)
############################################################
import datetime
import os
import re
import argparse
import json
import requests

def main():
  args=get_args(ver)
  get_crossref(*get_input(args))


def get_crossref(x4_ref,file_dict,format,email,force0):

  global force

  force=force0

  (code,agency,range_type,range_min,range_max)=read_dict()

  reference=x4_ref.split(",")
  (ref_type,volume,issue,page,year)=anal_reference(reference)

  issn="00000000"
  for key in code:
    if code[key]==reference[1]:
      for range_min0, range_max0 in zip(range_min[key],range_max[key]):
        if range_type[key]=="V":
          if int(volume)>=range_min0 and int(volume)<=range_max0:
            issn=key 
            break

  (url,params)=get_url(email,"piped",issn,volume,issue,page,year)
  xref_out=requests.get(url, params=params)
  arr=xref_out.text.rstrip(os.linesep).split("|")
  doi=arr[-1]

  if doi=="":
    msg="CrossRef does not return a DOI."
    print_error_1(msg,"")

  elif format=="doi":
    print(doi)

  else:
    (url,params)=get_url(email,format,issn,volume,issue,page,year)
    xref_out=requests.get(url, params=params)

#   print(xref_out.url)         # print URL for submission to CrossRef
#   print(xref_out.status_code) # 200 -> successful
#   print(xref_out.encoding)    # encoding type (json, text, ...)

    if format=="piped" or format=="xml":
      print(xref_out.text)

    elif format=="json":
      data=xref_out.json()
      char=json.dumps(data,indent=2)
      print(char)

  print("X4XREF: Processing terminated normally.")


def read_dict():

  code=dict()
  agency=dict()
  range_type=dict()
  range_min=dict()
  range_max=dict()

  file_dict="dict_arc_new.105"
  lines=get_file_lines(file_dict)
  for line in lines:
    line=line.rstrip(os.linesep)
    range_min0=[]
    range_max0=[]
    issn=line[12:20]                 # ISSN
    code[issn]=line[43:49].rstrip()  # EXFOR code
    agency[issn]=line[50:51]         # 1 -> CrossRef
    range_type[issn]=line[51:52]     # V -> volume, Y -> year

    for i in range(10):
      col_min=54+i*14
      col_max=col_min+7

      char_min=line[col_min-1:col_min+6].lstrip()
      char_max=line[col_max-1:col_max+6].lstrip()

      if i==0:
        if (char_min=="" and char_max==""):
          range_min0.append(0)
          range_max0.append(9999999)
          break
        elif (char_max==""):
          range_min0.append(int(char_min))
          range_max0.append(9999999)
          break
        elif (char_min==""):
          range_min0.append(0)
          range_max0.append(int(char_max))
        else:
          range_min0.append(int(char_min))
          range_max0.append(int(char_max))

      else:
        if (char_min==""):
          break
        elif (char_max==""):
          range_min0.append(int(char_min))
          range_max0.append(9999999)
          break
        else:
          range_min0.append(int(char_min))
          range_max0.append(int(char_max))

    range_min[issn]=range_min0
    range_max[issn]=range_max0

  return code,agency,range_type,range_min,range_max


def anal_reference(reference):

  ref_type=reference[0]

  date=reference[-1]

  if date[0:2]!="19" and date[0:2]!="20":
    date="19"+date
  year=date[0:4]

  if ref_type!="J":
    msg="Reference type "+ref_type+" is not supported."
    print_error_fatal(msg,"")

  if len(reference)!=5 and len(reference)!=6:
    msg="Too few or many comma separators: "+ reference
    print_error_fatal(msg,"")

  volume=reference[2]

  if len(reference)==5:
    issue=""
    page=reference[3]

  elif len(reference)==6:
    issue=reference[3]
    re.sub("^\(|\)$", "", issue)
    page=reference[4]

  return ref_type,volume,issue,page,year


def get_url(email,format,issn,volume,issue,page,year):
  fauthor=""
  doi=""

  url="https://doi.crossref.org/servlet/query"

# Example of Cross Ref API for N.Otuka+,J,NDS,120,272,2014 in piped format (to be abolished?)
#      https://doi.crossref.org/servlet/query?usr=email@address.com&format=json&qdata=00903752|||120||272|2014|||

# qdata=issn+"||"+fauthor+"|"+volume+"|"+issue+"|"+page+"|"+year+"|||"+doi

# Example of Cross Ref API for N.Otuka+,J,NDS,120,272,2014 in XML format
#      https://doi.crossref.org/servlet/query?usr=email@address.com&format=json&qdata=<?xml version = "1.0" encoding="UTF-8"?><query_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" xmlns="http://www.crossref.org/qschema/2.0"  xsi:schemaLocation="http://www.crossref.org/qschema/2.0 http://www.crossref.org/qschema/crossref_query_input2.0.xsd"><head><doi_batch_id>0000</doi_batch_id> </head><body><query><issn>00903752</issn><author match="fuzzy" search-all-authors="false">Otuka</author><volume>120</volume><issue></issue><first_page>272</first_page><year>2014</year></query></body></query_batch>

  qdata="<?xml version=\"1.0\" encoding=\"UTF-8\"?><query_batch xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" version=\"2.0\" xmlns=\"http://www.crossref.org/qschema/2.0\"  xsi:schemaLocation=\"http://www.crossref.org/qschema/2.0 http://www.crossref.org/qschema/crossref_query_input2.0.xsd\"><head><doi_batch_id>0000</doi_batch_id> </head><body><query>"
  qdata=qdata+"<issn>"+issn+"</issn><author match=\"fuzzy\" search-all-authors=\"false\">"+fauthor+"</author><volume>"+volume+"</volume><issue>"+issue+"</issue><first_page>"+page+"</first_page><year>"+year+"</year></query></body></query_batch>"
  
  params = {
             "usr": email,
             "format": format,
             "qdata": qdata
           } 

  return url,params
 

def get_args(ver):

  parser=argparse.ArgumentParser(\
   usage=" Get DOI for an EXFOR reference code",\
   epilog="example: x4_x4xref.py -c J,NDS,120,272,2014 -d dict_9130.json")
  parser.add_argument("-v", "--version",\
   action="version", version=ver)
  parser.add_argument("-f", "--force",\
   help="never prompt", action="store_true")
  parser.add_argument("-c", "--x4_ref",\
   help="EXFOR reference code")
  parser.add_argument("-d", "--file_dict",\
   help="name of input JSON dictionary")
  parser.add_argument("-r", "--format",\
   help="output format (doi, piped, json or xml)")
  parser.add_argument("-e", "--email",\
   help="your email address")

  args=parser.parse_args()
  return args


def get_input(args):
  time=datetime.datetime.now()
  date=time.strftime("%Y-%m-%d")
  print("X4XREF (Ver-"+ver+") run on "+date)
  print("-----------------------------------------")

  force0=args.force

  x4_ref=args.x4_ref
  if x4_ref is None:
    x4_ref=input("EXFOR reference code [J,NDS,120,272,2014] -> ")
    if x4_ref=="":
      x4_ref="J,NDS,120,272,2014"

  file_dict=args.file_dict
  if file_dict is None:
    file_dict=input("EXFOR/CINDA JSON Dict.[dict_9130.json] ----> ")
    if file_dict=="":
      file_dict="dict_9130.json"
  if not os.path.exists(file_dict):
    print(" ** File "+file_dict+" does not exist.")
  while not os.path.exists(file_dict):
    file_dict=input("EXFOR/CINDA JSON Dict.[dict_9130.json] ----> ")
    if file_dict=="":
      file_dict="dict_9130.json"
    if not os.path.exists(file_dict):
      print(" ** File "+file_dict+" does not exist.")

  format=args.format
  if format is None:
    format=input("Output format [doi] -----------------------> ")
    if format=="":
      format="doi"
  if format!="doi" and format!="piped" and format!="json" and format!="xml":
    print(" ** Format must be piped, json or xml.")
  while format!="doi" and format!="piped" and format!="json" and format!="xml":
    format=input("Output format [doi] -----------------------> ")
    if format!="doi" and format!="piped" and format!="json" and format!="xml":
      print(" ** Format must be doi, piped, json or xml.")

  email=args.email
  if email is None:
    email=input("Your email address ------------------------> ")
  if not re.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$").search(email):
    print(" ** Input a correct email address.")
  while not re.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$").search(email):
    email=input("Your email address ------------------------> ")
    if not re.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$").search(email):
      print(" ** Input a correct email address.")

  return x4_ref,file_dict,format,email,force0


def get_file_lines(file):
  if os.path.exists(file):
    f=open(file, "r")
    lines=f.readlines()
    f.close()
  else:
    msg="File "+file+" does not exist."
    print_error_fatal(msg)
  return lines


def print_error_fatal(msg,line):
  print("** "+msg)
  print(line)
  exit()


def print_error(msg,line,force):
  print("** "+msg)
  print(line)

  if force:
    answer="Y"
  else:
    answer=""

  while answer!="Y" and answer!="N":
    answer=input("Continue? [Y] --> ")
    if answer=="":
      answer="Y"
    if answer!="Y" and answer!="N":
      print(" ** Answer must be Y (Yes) or N (No).")
  if answer=="N":
    print("program terminated")
    exit()


def print_error_1(msg,line):
  print("**  "+msg)
  print(line)

  return


if __name__ == "__main__":
  main()
