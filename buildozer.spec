[app]
title = IPTV Player
package.name = iptvplayer
package.domain = com.hussam

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,kivy==2.1.0,requests

orientation = portrait
fullscreen = 0

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
