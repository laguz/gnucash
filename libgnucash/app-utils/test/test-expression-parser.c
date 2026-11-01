/********************************************************************\
 * test-expression-parser.c: Unit tests for calculation/expression_parser.c
 *                                                                  *
 * This program is free software; you can redistribute it and/or    *
 * modify it under the terms of the GNU General Public License as   *
 * published by the Free Software Foundation; either version 2 of   *
 * the License, or (at your option) any later version.              *
 *                                                                  *
 * This program is distributed in the hope that it will be useful,  *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of   *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the    *
 * GNU General Public License for more details.                     *
 *                                                                  *
 * You should have received a copy of the GNU General Public License*
 * along with this program; if not, contact:                        *
 *                                                                  *
 * Free Software Foundation           Voice:  +1-617-542-5942       *
 * 51 Franklin Street, Fifth Floor    Fax:    +1-617-542-2652       *
 * Boston, MA  02110-1301,  USA       gnu@gnu.org                   *
\********************************************************************/

#include <config.h>
#include <glib.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "finvar.h"
#include "finproto.h"
#include "fin_spl_protos.h"
#include "test-stuff.h"

/* Simple numeric representation using double for test purposes */
typedef struct
{
    double val;
} TestNum;

static void *
test_trans_numeric(const char *digit_str, gchar *radix_point, gchar *group_char, char **rstr)
{
    char *endptr;
    double d;

    if (!digit_str)
        return NULL;

    d = g_ascii_strtod(digit_str, &endptr);
    if (endptr == digit_str)
        return NULL;

    if (rstr)
        *rstr = endptr;

    TestNum *num = g_new0(TestNum, 1);
    num->val = d;
    return num;
}

static void *
test_numeric_ops(char op_sym, void *left_value, void *right_value)
{
    TestNum *l = (TestNum *)left_value;
    TestNum *r = (TestNum *)right_value;
    TestNum *res;

    if (!l || !r)
        return NULL;

    res = (op_sym == ASN_OP) ? l : g_new0(TestNum, 1);

    switch (op_sym)
    {
    case ADD_OP:
        res->val = l->val + r->val;
        break;
    case SUB_OP:
        res->val = l->val - r->val;
        break;
    case MUL_OP:
        res->val = l->val * r->val;
        break;
    case DIV_OP:
        res->val = (r->val != 0.0) ? (l->val / r->val) : 0.0;
        break;
    case ASN_OP:
        res->val = r->val;
        break;
    default:
        break;
    }

    return res;
}

static void *
test_negate_numeric(void *value)
{
    TestNum *num = (TestNum *)value;
    if (num)
        num->val = -num->val;
    return num;
}

static void
test_free_numeric(void *value)
{
    g_free(value);
}

static void *
test_func_op(const char *fname, int argc, void **argv)
{
    if (g_strcmp0(fname, "abs") == 0 && argc == 1)
    {
        var_store_ptr arg = (var_store_ptr)argv[0];
        if (arg && arg->type == VST_NUMERIC && arg->value)
        {
            TestNum *in = (TestNum *)arg->value;
            TestNum *out = g_new0(TestNum, 1);
            out->val = (in->val < 0.0) ? -in->val : in->val;
            return out;
        }
    }
    else if (g_strcmp0(fname, "add2") == 0 && argc == 2)
    {
        var_store_ptr a = (var_store_ptr)argv[0];
        var_store_ptr b = (var_store_ptr)argv[1];
        if (a && b && a->type == VST_NUMERIC && b->type == VST_NUMERIC)
        {
            TestNum *na = (TestNum *)a->value;
            TestNum *nb = (TestNum *)b->value;
            TestNum *out = g_new0(TestNum, 1);
            out->val = na->val + nb->val;
            return out;
        }
    }
    return NULL;
}

static parser_env_ptr
create_test_parser(var_store_ptr predefined_vars)
{
    return init_parser(predefined_vars, ".", ",",
                       test_trans_numeric,
                       test_numeric_ops,
                       test_negate_numeric,
                       test_free_numeric,
                       test_func_op);
}

static void
test_init_and_exit(void)
{
    parser_env_ptr pe = create_test_parser(NULL);
    do_test(pe != NULL, "init_parser should return non-NULL");
    do_test(get_parse_error(pe) == PARSER_NO_ERROR, "initial error code should be PARSER_NO_ERROR");
    do_test(parser_get_vars(pe) == NULL, "initial named vars should be NULL");
    exit_parser(pe);

    /* Test NULL-safety */
    exit_parser(NULL);
    do_test(get_parse_error(NULL) == PARSER_NO_ERROR, "get_parse_error(NULL) should be PARSER_NO_ERROR");
    do_test(parser_get_vars(NULL) == NULL, "parser_get_vars(NULL) should be NULL");
    do_test(delete_var("xyz", NULL) == FALSE, "delete_var with NULL parser returns FALSE");
    do_test(parse_string(NULL, NULL, NULL) == NULL, "parse_string with NULL arguments returns NULL");
}

static void
test_basic_arithmetic(void)
{
    parser_env_ptr pe = create_test_parser(NULL);
    var_store result;
    char *err_pos;

    /* Addition */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "12 + 34", pe);
    do_test(err_pos == NULL, "parse '12 + 34' error position should be NULL");
    do_test(get_parse_error(pe) == PARSER_NO_ERROR, "error code should be PARSER_NO_ERROR");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 46.0, "12 + 34 = 46");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Subtraction */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "50 - 18", pe);
    do_test(err_pos == NULL, "parse '50 - 18' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 32.0, "50 - 18 = 32");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Multiplication */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "6 * 7", pe);
    do_test(err_pos == NULL, "parse '6 * 7' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 42.0, "6 * 7 = 42");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Division */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "100 / 4", pe);
    do_test(err_pos == NULL, "parse '100 / 4' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 25.0, "100 / 4 = 25");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Operator precedence: 2 + 3 * 4 = 14, not 20 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "2 + 3 * 4", pe);
    do_test(err_pos == NULL, "parse '2 + 3 * 4' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 14.0, "precedence 2 + 3 * 4 = 14");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Parentheses */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "(2 + 3) * 4", pe);
    do_test(err_pos == NULL, "parse '(2 + 3) * 4' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 20.0, "(2 + 3) * 4 = 20");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Unary minus & plus */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "-5 + +3", pe);
    do_test(err_pos == NULL, "parse '-5 + +3' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == -2.0, "-5 + +3 = -2");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* (num) syntax interpreted as -num */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "(42)", pe);
    do_test(err_pos == NULL, "parse '(42)' error position should be NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == -42.0, "(42) = -42");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    exit_parser(pe);
}

static void
test_variables_and_assignments(void)
{
    parser_env_ptr pe = create_test_parser(NULL);
    var_store result;
    char *err_pos;
    var_store_ptr vars;

    /* Assignment: x = 10 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x = 10", pe);
    do_test(err_pos == NULL, "parse 'x = 10' error pos NULL");
    do_test(get_parse_error(pe) == PARSER_NO_ERROR, "error code PARSER_NO_ERROR");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 10.0, "x = 10 returned value 10");

    vars = parser_get_vars(pe);
    do_test(vars != NULL, "named variables list non-NULL");
    do_test(g_strcmp0(vars->variable_name, "x") == 0, "variable named 'x' exists");
    do_test(((TestNum *)vars->value)->val == 10.0, "variable 'x' has value 10");

    /* Using variable: x + 5 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x + 5", pe);
    do_test(err_pos == NULL, "parse 'x + 5' error pos NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 15.0, "x + 5 = 15");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Compound assignments: +=, -=, *=, /= */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x += 5", pe);
    do_test(err_pos == NULL, "parse 'x += 5' succeeded");
    do_test(((TestNum *)result.value)->val == 15.0, "x += 5 results in 15");

    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x -= 3", pe);
    do_test(err_pos == NULL, "parse 'x -= 3' succeeded");
    do_test(((TestNum *)result.value)->val == 12.0, "x -= 3 results in 12");

    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x *= 2", pe);
    do_test(err_pos == NULL, "parse 'x *= 2' succeeded");
    do_test(((TestNum *)result.value)->val == 24.0, "x *= 2 results in 24");

    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "x /= 4", pe);
    do_test(err_pos == NULL, "parse 'x /= 4' succeeded");
    do_test(((TestNum *)result.value)->val == 6.0, "x /= 4 results in 6");

    /* Multiple assignments: a = b = 7 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "a = b = 7", pe);
    do_test(err_pos == NULL, "parse 'a = b = 7' succeeded");
    do_test(((TestNum *)result.value)->val == 7.0, "a = b = 7 results in 7");

    /* delete_var */
    do_test(delete_var("nonexistent", pe) == FALSE, "delete nonexistent variable returns FALSE");
    do_test(delete_var("a", pe) == TRUE, "delete variable 'a' returns TRUE");
    do_test(delete_var("a", pe) == FALSE, "delete variable 'a' again returns FALSE");

    exit_parser(pe);
}

static void
test_predefined_vars(void)
{
    var_store predefined;
    TestNum pre_val;
    parser_env_ptr pe;
    var_store result;
    char *err_pos;

    pre_val.val = 100.0;
    predefined.variable_name = "CONST_VAL";
    predefined.use_flag = USED_VAR;
    predefined.assign_flag = ASSIGNED_TO;
    predefined.type = VST_NUMERIC;
    predefined.value = &pre_val;
    predefined.next_var = NULL;

    pe = create_test_parser(&predefined);

    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "CONST_VAL * 2", pe);
    do_test(err_pos == NULL, "parse 'CONST_VAL * 2' error pos NULL");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 200.0, "CONST_VAL * 2 = 200");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    exit_parser(pe);
}

static void
test_functions(void)
{
    parser_env_ptr pe = create_test_parser(NULL);
    var_store result;
    char *err_pos;

    /* Function with 1 argument: abs(-15) */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "abs(-15)", pe);
    do_test(err_pos == NULL, "parse 'abs(-15)' succeeded");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 15.0, "abs(-15) = 15");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Function with 2 arguments separated by colon: add2(10 : 25) */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "add2(10 : 25)", pe);
    do_test(err_pos == NULL, "parse 'add2(10 : 25)' succeeded");
    do_test(result.value != NULL && ((TestNum *)result.value)->val == 35.0, "add2(10 : 25) = 35");
    if (!result.variable_name && result.value)
        test_free_numeric(result.value);

    /* Unknown function: unknown_fn(1) -> error */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "unknown_fn(1)", pe);
    do_test(err_pos != NULL, "parse unknown function returns error pos");
    do_test(get_parse_error(pe) != PARSER_NO_ERROR, "error code should not be PARSER_NO_ERROR for unknown function");

    exit_parser(pe);
}

static void
test_error_handling(void)
{
    parser_env_ptr pe = create_test_parser(NULL);
    var_store result;
    char *err_pos;

    /* NULL string input */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, NULL, pe);
    do_test(err_pos == NULL, "parse_string(NULL) returns NULL");

    /* Empty string */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "", pe);
    do_test(err_pos != NULL, "empty string returns error pos");
    do_test(get_parse_error(pe) == STACK_UNDERFLOW, "empty string results in STACK_UNDERFLOW");

    /* Incomplete expression with operator at end: (5 + 23)/ */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "(5 + 23)/", pe);
    do_test(err_pos != NULL, "incomplete expression returns error pos");
    do_test(get_parse_error(pe) != PARSER_NO_ERROR, "incomplete expression produces parse error");

    /* Undefined character: 1 @ 2 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "1 @ 2", pe);
    do_test(err_pos != NULL, "undefined char returns error pos");
    do_test(get_parse_error(pe) == UNDEFINED_CHARACTER, "error UNDEFINED_CHARACTER");

    /* Not a variable assignment: 5 = 10 */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "5 = 10", pe);
    do_test(err_pos != NULL, "assigning to number returns error pos");
    do_test(get_parse_error(pe) != PARSER_NO_ERROR, "error code should not be PARSER_NO_ERROR for invalid assignment");

    /* Grammar error: consecutive numbers without operator "1 2" */
    memset(&result, 0, sizeof(result));
    err_pos = parse_string(&result, "1 2", pe);
    do_test(err_pos != NULL, "grammar error returns error pos");
    do_test(get_parse_error(pe) != PARSER_NO_ERROR, "error code should not be PARSER_NO_ERROR for grammar error");

    exit_parser(pe);
}

int
main(int argc, char **argv)
{
    test_init_and_exit();
    test_basic_arithmetic();
    test_variables_and_assignments();
    test_predefined_vars();
    test_functions();
    test_error_handling();

    print_test_results();
    return get_rv();
}
