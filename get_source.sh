#!/bin/bash
set -e

VERSION="2.5.0"
ARCHIVE="v${VERSION}.tar.gz"
URL="https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/${ARCHIVE}"

mkdir -p source
cd source

if [ -f "$ARCHIVE" ]; then
    file_type=$(file -b --mime-type "$ARCHIVE")
    if [[ "$file_type" != "application/gzip" ]]; then
        echo "⚠️ Removing invalid archive: $ARCHIVE"
        rm -f "$ARCHIVE"
    fi
fi

if [ ! -f "$ARCHIVE" ]; then
    echo "📥 Downloading OpenColorIO ${VERSION}..."
    curl -L -o "$ARCHIVE" "$URL"
fi

rm -rf OpenColorIO-${VERSION}
tar -xzf "$ARCHIVE"

git clone https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES.git configs/aces_1.3


echo "✅ OpenColorIO source ready"

