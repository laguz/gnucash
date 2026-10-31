#include <kvp-frame.hpp>

#include <config.h>

#include <stdlib.h>

#include "test-stuff.h"
#include "test-engine-stuff.h"

#include "qof.h"

#include "test-file-stuff.h"
#include "sixtp-dom-generators.h"
#include "sixtp-dom-parsers.h"

#define GNC_V2_STRING "gnc-v2"
const gchar* gnc_v2_xml_version_string = GNC_V2_STRING;
extern KvpFrame* dom_tree_to_kvp_frame (xmlNodePtr node);

static void
test_kvp_get_slot (int run,
                   KvpFrame* test_frame1, const KvpValue* test_val1,
                   const gchar* test_key)
{
    auto test_val2 = test_frame1->get_slot ({test_key});
    auto msg = "KvpFrame::get_slot";
    if (compare (test_val1, test_val2) == 0)
    {
        success_args (msg, __FILE__, __LINE__, "run=%d", run);
    }
    else
    {
        failure_args (msg, __FILE__, __LINE__, "run=%d", run);
        printf ("    Value is %s\n", test_val2->to_string ().c_str ());
    }
}

static void
test_kvp_copy_compare (int run,
                       KvpFrame* test_frame1, const KvpValue* test_val1,
                       const gchar* test_key)
{
    auto test_frame2 = new KvpFrame (*test_frame1);
    auto msg = "compare after KvpFrame copy construction";
    do_test_args (test_frame2 != NULL, "KvpFrame Copy Constructor",
                  __FILE__, __LINE__, "run=%d", run);

    if (compare (test_frame1, test_frame2) == 0)
    {
        success_args (msg, __FILE__, __LINE__, "run=%d", run);
    }
    else
    {
        failure_args (msg, __FILE__, __LINE__, "run=%d", run);
        printf ("Frame1 is %s\n", test_frame1->to_string ().c_str ());
        printf ("Frame2 is %s\n", test_frame2->to_string ().c_str ());
    }

    delete test_frame2;
}

static void
test_kvp_copy_get_slot (int run,
                        KvpFrame* test_frame1, const KvpValue* test_val1,
                        const gchar* test_key)
{
    auto test_frame2 = new KvpFrame (*test_frame1);
    auto test_val2 = test_frame2->get_slot ({test_key});
    auto msg = "KvpFrame::get_slot() from a copy-constructed frame";
    if (compare (test_val1, test_val2) == 0)
    {
        success_args (msg, __FILE__, __LINE__, "run=%d", run);
    }
    else
    {
        failure_args (msg, __FILE__, __LINE__, "run=%d", run);
        printf ("Frame1 is %s\n", test_frame1->to_string ().c_str ());
        printf ("Frame2 is %s\n", test_frame2->to_string ().c_str ());
    }
    delete test_frame2;
}

static void
test_kvp_create_delete (void)
{
    auto test_frame = new KvpFrame;
    auto msg = "KvpFrame default constructor";
    if (test_frame != nullptr)
    {
        delete test_frame;
        test_frame = nullptr;
        success (msg);
    }
    else
    {
        failure (msg);
    }
}

static void
test_kvp_frames1 (void)
{
    int i;

    for (i = 0; i < 20; i++)
    {
        auto test_val1 = get_random_kvp_value (i % KvpValue::Type::FRAME);
        auto test_frame1 = new KvpFrame;
        auto test_key = get_random_string_without ("/");

        test_frame1->set ({test_key}, test_val1);

        test_kvp_get_slot (i, test_frame1, test_val1, test_key);
        test_kvp_copy_compare (i, test_frame1, test_val1, test_key);
        test_kvp_copy_get_slot (i, test_frame1, test_val1, test_key);

        g_free (test_key);
        delete test_frame1;
    }
}

static void
test_kvp_printing (void)
{
    int i;
    for (i = 0; i < 20; i++)
    {
        auto ran_frame = get_random_kvp_frame ();
        assert (!ran_frame->to_string ().empty ());
        delete ran_frame;
    }
}

static void
test_kvp_xml_stuff (void)
{
    int i;
    for (i = 0; i < 20; i++)
    {
        auto inst = static_cast<QofInstance*> (g_object_new (QOF_TYPE_INSTANCE, NULL));
        KvpFrame* test_frame2;
        xmlNodePtr test_node;

        inst->kvp_data = get_random_kvp_frame ();
        auto msg = "XML Stuff";

        test_node = qof_instance_slots_to_dom_tree ("test-kvp", inst);

        if (!test_node)
        {
            failure_args ("xml stuff", __FILE__, __LINE__,
                          "kvp_frame_to_dom_tree produced NULL");
        }
        else
        {
            test_frame2 = dom_tree_to_kvp_frame (test_node);

            if (compare (inst->kvp_data, test_frame2) == 0)
            {
                success (msg);
            }
            else
            {
                failure (msg);
                printf ("  With KvpFrame 1:\n%s\n",
                        inst->kvp_data->to_string ().c_str ());
                printf ("  and XML:\n");
                xmlElemDump (stdout, NULL, test_node);
                printf ("\n   and kvp_frame 2:\n%s\n",
                        test_frame2->to_string ().c_str ());
            }
            delete test_frame2;
            xmlFreeNode (test_node);
        }
        g_object_unref (inst);
    }
}

static void
test_kvp_unknown_type (void)
{
    /* Test unknown type tag handling in dom_tree_to_kvp_frame */
    xmlNodePtr root = xmlNewNode (NULL, BAD_CAST "test-kvp");
    xmlNodePtr slot1 = xmlNewChild (root, NULL, BAD_CAST "slot", NULL);
    xmlNewChild (slot1, NULL, BAD_CAST "slot:key", BAD_CAST "bad-type-key");
    xmlNodePtr val1 = xmlNewChild (slot1, NULL, BAD_CAST "slot:value", BAD_CAST "some content");
    xmlSetProp (val1, BAD_CAST "type", BAD_CAST "unknown-custom-type");

    xmlNodePtr slot2 = xmlNewChild (root, NULL, BAD_CAST "slot", NULL);
    xmlNewChild (slot2, NULL, BAD_CAST "slot:key", BAD_CAST "no-type-key");
    xmlNewChild (slot2, NULL, BAD_CAST "slot:value", BAD_CAST "some content");

    xmlNodePtr slot3 = xmlNewChild (root, NULL, BAD_CAST "slot", NULL);
    xmlNewChild (slot3, NULL, BAD_CAST "slot:key", BAD_CAST "valid-key");
    xmlNodePtr val3 = xmlNewChild (slot3, NULL, BAD_CAST "slot:value", BAD_CAST "12345");
    xmlSetProp (val3, BAD_CAST "type", BAD_CAST "integer");

    auto frame = dom_tree_to_kvp_frame (root);
    do_test_args (frame != nullptr, "dom_tree_to_kvp_frame with unknown type returns valid frame",
                  __FILE__, __LINE__, "");
    if (frame)
    {
        do_test_args (frame->get_slot ({"bad-type-key"}) == nullptr,
                      "unknown type slot was ignored", __FILE__, __LINE__, "");
        do_test_args (frame->get_slot ({"no-type-key"}) == nullptr,
                      "no type slot was ignored", __FILE__, __LINE__, "");
        auto valid_val = frame->get_slot ({"valid-key"});
        do_test_args (valid_val != nullptr && valid_val->get<int64_t>() == 12345,
                      "valid slot was parsed correctly", __FILE__, __LINE__, "");
        delete frame;
    }
    xmlFreeNode (root);
}

int
main (int argc, char** argv)
{
    qof_init ();
    test_kvp_create_delete ();
    test_kvp_printing ();
    test_kvp_frames1 ();
    test_kvp_xml_stuff ();
    test_kvp_unknown_type ();
    print_test_results ();
    exit (get_rv ());
}
