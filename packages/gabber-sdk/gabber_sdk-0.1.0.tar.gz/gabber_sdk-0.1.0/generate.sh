set -e
rm -rf gabber/generated/gabber
rm -rf gabber/generated/gabber_internal

openapi-generator generate \
    -i ~/gabber-backend/assets/openapi/openapi.yaml \
    -g python \
    --global-property=generateAliasAsModel=false \
    --additional-properties=library=asyncio,packageName=gabber.generated.gabber,generateSourceCodeOnly=true
    
openapi-generator generate \
    -i ~/gabber-backend/assets/openapi/openapi-internal.yaml \
    -g python \
    --additional-properties=library=asyncio,packageName=gabber.generated.gabber_internal,generateSourceCodeOnly=true
