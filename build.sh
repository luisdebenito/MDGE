#!/bin/sh

rm -rf build/
export SPEED_RATIO=6
pygbag --can_close 1 --build --no_opt .
mkdir build/web/media
cp -R media/* build/web/media/
rm build/web/favicon.png
mv build/web/media/favicon.png build/web/favicon.png
git checkout webapp
mv build/web/* .