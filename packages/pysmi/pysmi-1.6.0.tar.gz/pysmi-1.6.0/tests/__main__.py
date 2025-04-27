#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
try:
    import unittest2 as unittest

except ImportError:
    import unittest

suite = unittest.TestLoader().loadTestsFromNames(
    [
        "test_zipreader",
        "test_agentcapabilities_smiv2_pysnmp",
        "test_defval_smiv2_pysnmp",
        "test_imports_smiv2_pysnmp",
        "test_modulecompliance_smiv2_pysnmp",
        "test_moduleidentity_smiv2_pysnmp",
        "test_notificationgroup_smiv2_pysnmp",
        "test_notificationtype_smiv2_pysnmp",
        "test_objectgroup_smiv2_pysnmp",
        "test_objectidentity_smiv2_pysnmp",
        "test_objecttype_smiv1_pysnmp",
        "test_objecttype_smiv2_pysnmp",
        "test_smiv1_smiv2_pysnmp",
        "test_syntaxname_smiv2_pysnmp",
        "test_traptype_smiv1_pysnmp",
        "test_typedeclaration_smiv1_pysnmp",
        "test_typedeclaration_smiv2_pysnmp",
        "test_valuedeclaration_smiv2_pysnmp",
    ]
)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
