#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
import sys
import textwrap

try:
    import unittest2 as unittest

except ImportError:
    import unittest

from pysmi.parser.smi import parserFactory
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.codegen.symtable import SymtableCodeGen
from pysnmp.smi.builder import MibBuilder


class ObjectTypeBasicTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "seconds"
        MAX-ACCESS      accessible-for-notify
        STATUS          current
        DESCRIPTION     "Test object"
        REFERENCE       "ABC"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSymbol(self):
        self.assertTrue("testObjectType" in self.ctx, "symbol not present")

    def testObjectTypeName(self):
        self.assertEqual(self.ctx["testObjectType"].getName(), (1, 3), "bad name")

    def testObjectTypeDescription(self):
        self.assertEqual(
            self.ctx["testObjectType"].getDescription(),
            "Test object",
            "bad DESCRIPTION",
        )

    def testObjectTypeStatus(self):
        self.assertEqual(
            self.ctx["testObjectType"].getStatus(), "current", "bad STATUS"
        )

    def testObjectTypeReference(self):
        self.assertEqual(
            self.ctx["testObjectType"].getReference(),
            "ABC",
            "bad REFERENCE",
        )

    def testObjectTypeMaxAccess(self):
        self.assertEqual(
            self.ctx["testObjectType"].getMaxAccess(),
            "accessible-for-notify",
            "bad MAX-ACCESS",
        )

    def testObjectTypeUnits(self):
        self.assertEqual(self.ctx["testObjectType"].getUnits(), "seconds", "bad UNITS")

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(123), 123, "bad SYNTAX"
        )

    def testObjectTypeClass(self):
        self.assertEqual(
            self.ctx["testObjectType"].__class__.__name__, "MibScalar", "bad SYNTAX"
        )


class ObjectTypeHyphenTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    test-object-type OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "seconds"
        MAX-ACCESS      accessible-for-notify
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSymbol(self):
        self.assertTrue("test_object_type" in self.ctx, "symbol not present")

    def testObjectTypeLabel(self):
        self.assertEqual(
            self.ctx["test_object_type"].getLabel(), "test-object-type", "bad label"
        )


class ObjectTypeTextTestCase(unittest.TestCase):
    R"""
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "lines per
    text block"
        MAX-ACCESS      accessible-for-notify
        STATUS          deprecated
        DESCRIPTION     "Test
                         object\n"
        REFERENCE       "ABC\"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        docstring = textwrap.dedent(self.__class__.__doc__)
        ast = parserFactory()().parse(docstring)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast,
            {mibInfo.name: symtable},
            genTexts=True,
            textFilter=lambda symbol, text: text,
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeStatus(self):
        # Use a value other than "current" in this test, as "current" is the
        # default pysnmp value (which could mean the test value was never set).
        self.assertEqual(
            self.ctx["testObjectType"].getStatus(), "deprecated", "bad SYNTAX"
        )

    def testObjectTypeDescription(self):
        self.assertEqual(
            self.ctx["testObjectType"].getDescription(),
            "Test\n                     object\\n",
            "bad DESCRIPTION",
        )

    def testObjectTypeReference(self):
        self.assertEqual(
            self.ctx["testObjectType"].getReference(), "ABC\\", "bad REFERENCE"
        )

    def testObjectTypeUnits(self):
        self.assertEqual(
            self.ctx["testObjectType"].getUnits(), "lines per\ntext block", "bad UNITS"
        )


class ObjectTypeNoLoadTextsTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "seconds"
        MAX-ACCESS      accessible-for-notify
        STATUS          obsolete
        DESCRIPTION     "Test object"
        REFERENCE       "ABC"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeStatus(self):
        # "current" is the default pysnmp value, and therefore what we get if
        # we request that texts not be loaded.
        self.assertEqual(
            self.ctx["testObjectType"].getStatus(), "current", "bad STATUS"
        )

    def testObjectTypeDescription(self):
        self.assertEqual(
            self.ctx["testObjectType"].getDescription(),
            "",
            "bad DESCRIPTION",
        )

    def testObjectTypeReference(self):
        self.assertEqual(self.ctx["testObjectType"].getReference(), "", "bad REFERENCE")

    def testObjectTypeUnits(self):
        self.assertEqual(self.ctx["testObjectType"].getUnits(), "", "bad UNITS")


class ObjectTypeWithIntegerConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Unsigned32 (0..4294967295)
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(123),
            123,
            "bad integer range constrained SYNTAX",
        )


class ObjectTypeWithIntegerSetConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Unsigned32 (0|2|44)
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(44),
            44,
            "bad multiple integer constrained SYNTAX",
        )


class ObjectTypeWithStringSizeConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          OCTET STRING (SIZE (0..512))
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(""),
            b"",
            "bad size constrained SYNTAX",
        )


class ObjectTypeBitsTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          BITS { notification(0), set(1) }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(("set",)),
            b"@",
            "bad BITS SYNTAX",
        )


class ObjectTypeMibTableTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER,
            testValue   OCTET STRING
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testValue OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 2 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )

    def testObjectTypeTableColumnClass(self):
        self.assertEqual(
            self.ctx["testIndex"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"),),
            "bad table index",
        )


class ObjectTypeMibTableImpliedIndexTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { IMPLIED testIndex }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((1, "TEST-MIB", "testIndex"),),
            "bad IMPLIED table index",
        )


class ObjectTypeMibTableMultipleIndicesTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex, testValue }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER,
            testValue   OCTET STRING
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testValue OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 2 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"), (0, "TEST-MIB", "testValue")),
            "bad multiple table indices",
        )


class ObjectTypeAugmentingMibTableTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testTableExt OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntryExt
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 4 }

      testEntryExt OBJECT-TYPE
        SYNTAX          TestEntryExt
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        AUGMENTS        { testEntry }
      ::= { testTableExt 3 }

      TestEntryExt ::= SEQUENCE {
            testIndexExt   INTEGER
      }

      testIndexExt OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntryExt 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowAugmention(self):
        # TODO: provide getAugmentation() method
        try:
            augmentingRows = self.ctx["testEntry"].augmentingRows

        except AttributeError:
            augmentingRows = self.ctx["testEntry"]._augmentingRows

        self.assertEqual(
            list(augmentingRows)[0],
            ("TEST-MIB", "testEntryExt"),
            "bad AUGMENTS table clause",
        )


class ObjectTypeMibTableHyphenTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    -- deliberately moved up
    test-index OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { test-entry 1 }

    test-table OBJECT-TYPE
        SYNTAX          SEQUENCE OF Test-Entry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

    test-entry OBJECT-TYPE
        SYNTAX          Test-Entry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { test-index, global }
      ::= { test-table 3 }

    Test-Entry ::= SEQUENCE {
        test-index  INTEGER,
        global      OCTET STRING  -- a reserved Python keyword
    }

    global OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { test-entry 2 }

    test-table-ext OBJECT-TYPE
        SYNTAX          SEQUENCE OF Test-Entry-Ext
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 4 }

    test-entry-ext OBJECT-TYPE
        SYNTAX          Test-Entry-Ext
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        AUGMENTS        { test-entry }
      ::= { test-table-ext 3 }

    Test-Entry-Ext ::= SEQUENCE {
        testIndexExt   INTEGER
    }

    testIndexExt OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { test-entry-ext 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["test_table"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["test_entry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )

    def testObjectTypeTableColumnClass1(self):
        self.assertEqual(
            self.ctx["test_index"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableColumnClass2(self):
        self.assertEqual(
            self.ctx["_pysmi_global"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["test_entry"].getIndexNames(),
            ((0, "TEST-MIB", "test-index"), (0, "TEST-MIB", "global")),
            "bad table indices",
        )

    def testObjectTypeTableRowAugmention(self):
        # TODO: provide getAugmentation() method
        try:
            augmentingRows = self.ctx["test_entry"].augmentingRows

        except AttributeError:
            augmentingRows = self.ctx["test_entry"]._augmentingRows

        self.assertEqual(
            list(augmentingRows)[0],
            ("TEST-MIB", "test-entry-ext"),
            "bad AUGMENTS table clause",
        )

    def testObjectTypeTableAugRowIndex(self):
        self.assertEqual(
            self.ctx["test_entry_ext"].getIndexNames(),
            ((0, "TEST-MIB", "test-index"), (0, "TEST-MIB", "global")),
            "bad table indices",
        )


# This case verifies that pysmi provides leniency for a type name mismatch in
# "SEQUENCE OF" syntaxes for conceptual-table object types, as long as the
# corresponding table entry object type is correct.
class ObjectTypeMibTableMismatchedSequenceOfTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TypoEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          Test-Entry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      Test-Entry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )

    def testObjectTypeTableColumnClass(self):
        self.assertEqual(
            self.ctx["testIndex"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"),),
            "bad table index",
        )


class ObjectTypeMibTableAndColumnTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      Overview ::= SEQUENCE {
            testTable   TestEntry
      }

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
