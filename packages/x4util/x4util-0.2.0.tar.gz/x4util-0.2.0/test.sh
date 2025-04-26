#!/bin/dash
RELEASE_VERSION='0.1.1.dev0'
PACKAGE_JSON_URL="https://test.pypi.org/pypi/x4util/json"
AVAIL_VERSIONS=$(curl -L -s $PACKAGE_JSON_URL | jq  -r '.releases | keys | .[]' | sort -V)
echo "Available versions: $AVAIL_VERSIONS"

case "*$RELEASE_VERSION*" in 
  $AVAIL_VERSIONS )
    echo "Available versions ($AVAIL_VERSIONS) contain release version ($RELEASE_VERSION)"
    ;;
esac



case "$AVAIL_VERSIONS" in
    *"$RELEASE_VERSION"* )
         echo "do something with $RELEASE_VERSION"
         ;;
esac 

exit 0

string='My long string'

if printf "$AVAIL_VERSIONS" | grep "0.1.1"; then
  echo "It's there!"
fi