# build 
sphinx-build -T -b gettext docs docs/_build/gettext

for FILEPATH in $(find docs/_build/gettext -name '*.pot'); do
    if echo $FILEPATH | grep "docs/_build/gettext/coverage.pot"; then
        continue
    fi
    if echo $FILEPATH | grep  "docs/_build/gettext/changelog"; then
        continue
    fi

    RESOURCE_SLUG=$(echo $FILEPATH | sed 's/docs\/_build\/gettext\///' | sed 's/.pot//' | tr "/" "_" )
    FILE_FILTER=$(echo $FILEPATH | sed 's/build\/gettext/locales\/<lang>\/LC_MESSAGES/' | sed 's/.$//')
    SOURCE_FILE=$FILEPATH
    
    tx add \
        --organization vyos \
        --project sagitta \
        --resource $RESOURCE_SLUG \
        --resource-name $RESOURCE_SLUG \
        --file-filter "$FILE_FILTER" \
        --type PO \
        $FILEPATH
done