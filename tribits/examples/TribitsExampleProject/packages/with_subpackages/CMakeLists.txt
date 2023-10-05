tribits_package_decl(WithSubpackages)

tribits_add_debug_option()

if (WithSubpackagesB_DISABLE_SUPPORT_FOR_MixedLang)
  tribits_disable_optional_dependency(MixedLang
    "WithSubpackagesB: Disabling support for MixedLang because WithSubpackagesB_DISABLE_SUPPORT_FOR_MixedLang='${WithSubpackagesB_DISABLE_SUPPORT_FOR_MixedLang}'!"
    PACKAGE_NAME WithSubpackagesB)
endif()

tribits_process_subpackages()

tribits_exclude_files(
  b/ExcludeFromRelease.txt
  b/src/AlsoExcludeFromTarball.txt
  )

tribits_package_def()

tribits_package_postprocess()
