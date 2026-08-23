[app]

# (str) Title of your application
title = yt2ez

# (str) Package name
package.name = yt2ez

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yt2ez

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3,ogg,wav,exe

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,yt-dlp,certifi,charset-normalizer,idna,requests,urllib3,mutagen,brotli,pyjnius

# (str) Custom source folders for requirements
# Requirements will be searched in these directories in order
# requirements.source = /path/to/local/pip/packages, /path/to/local/python/packages

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRY_POINT_TO_PY,NAME2:ENTRY_POINT_TO_PY2

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.1.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format
# see https://lottiefiles.com/ for examples
#android.presplash_lottie = %(source.dir)s/presplash.json

# (str) Adaptive icon (used as default icon if icon.filename is not set)
#android.adaptive_icon = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (list) Features (adds uses-feature -tags to manifest)
#android.features = android.hardware.camera.front

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 24

# (bool) Use --private data storage (True) or dir public (False)
android.private_storage = False

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any internet access during the build
#android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements the Android Activity
# Use that parameter together with android.entrypoint to use a custom activity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# Use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml = %(source.dir)s/extra_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> tag of AndroidManifest.xml
#android.extra_manifest_application_xml = %(source.dir)s/extra_manifest_application.xml

# (str) Full name including package path of the Java class that implements the PythonService
# Use it together with services to use a custom service class
#android.service_class_name = org.kivy.android.PythonService

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android application uses fullscreen
#android.fullscreen = False

# (str) Copy these files to src/main/assets (use for data files)
#android.assets = data/*

# (str) Assets directory to include (for data files)
#android.assets_dir = %(source.dir)s/assets

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (list) Add android compile options
#android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add
#android.gradle_repositories =

# (str) Python-for-android branch to use, if not master you can try develop or a tag
#p4a.branch = master

# (str) OUYA Console category (game or app)
#android.ouya.category = game

# (str) Filename of OUYA Console icon
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML to include in the AndroidManifest.xml <intent-filter> of the main activity
#android.manifest_intent_filters =

# (str) Copy these libraries to the Android APK (useful for custom C libraries)
#android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
#android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

# (bool) Use old Gradle 4.0
#android.gradle_4 = False

# (str) Extra arguments to pass to gradlew
#android.gradle_args =

# (bool) Enable AndroidX (required for API 28+)
android.enable_androidx = True

# (str) Gradle plugin version
android.gradle_plugin = 7.3.0

# (str) Kotlin version
android.kotlin_version = 1.7.10

# (bool) If True, use python-for-android's native build of SDL2
#android.use_sdl2 = True

# (str) The Android architecture to build for (arm64-v8a, armeabi-v7a, x86, x86_64)
# You can specify multiple architectures
android.archs = arm64-v8a,armeabi-v7a

# (bool) If True, build a multi-arch APK (contains both arm64-v8a and armeabi-v7a)
#android.multiarch = True

# (bool) If True, build AAB instead of APK
android.aab = False

#
# iOS specific
#

# (str) Path to the certificate file for code signing
#ios.codesign.cert = 

# (str) Path to the provisioning profile
#ios.codesign.profile = 

# (str) Name of the provisioning profile
#ios.codesign.name = 

# (str) App Store Team ID
#ios.codesign.team = 

# (str) The iOS application bundle ID
#ios.bundle_id = 

# (str) The iOS application name
#ios.app_name = 

# (str) The iOS application version
#ios.version = 

# (str) The iOS application build number
#ios.build = 

# (str) URL of the iOS application icon
#ios.icon = 

# (str) URL of the iOS application launch image
#ios.launch_image = 

# (str) iOS Device family (1=iPhone, 2=iPad, 3=Universal)
#ios.device_family = 3

# (str) iOS minimum version
#ios.min_version = 13.0

# (str) iOS SDK to use
#ios.sdk = 

# (list) iOS frameworks to link
#ios.frameworks = 

# (list) iOS libraries to link
#ios.libraries = 

# (bool) iOS application uses fullscreen
#ios.fullscreen = True

# (str) iOS orientation
#ios.orientation = portrait

#
# Buildozer specific
#

# (int) Log level (0 = debug, 1 = info, 2 = warning, 3 = error)
log_level = 1

# (bool) Warn if buildozer is not the latest version
warn_on_root = 1

# (str) Path to buildozer cache directory
#buildozer.cache_dir = ~/.buildozer

# (bool) If True, clean buildozer cache before building
#buildozer.clean_cache = False

# (bool) If True, print command before executing
#buildozer.verbose = False