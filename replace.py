import re

with open("gnucash/gnome-utils/gnc-recurrence.c", "r") as f:
    content = f.read()

replacement = """
    if (pt == GNCR_MONTH && g_date_valid(&start))
    {
        int week = 0;
        int day_of_month_index = 0;
        const char *numerals[] = {N_("1st"), N_("2nd"), N_("3rd"), N_("4th")};
        gchar day_name_buf[10];
        gchar *label;

        gnc_dow_abbrev(day_name_buf, 10, g_date_get_weekday(&start) % 7);
        day_of_month_index = g_date_get_day(&start) - 1;
        week = day_of_month_index / 7 > 3 ? 3 : day_of_month_index / 7;

        label = g_strdup_printf(_("%s %s"), _(numerals[week]), day_name_buf);
        gtk_button_set_label(GTK_BUTTON(gr->nth_weekday), label);
        g_free(label);

        if (use_wd)
            label = g_strdup_printf(_("last %s"), day_name_buf);
        else
            label = g_strdup(_("last of month"));
        gtk_button_set_label(GTK_BUTTON(gr->gcb_eom), label);
        g_free(label);
    }
"""

new_content = content.replace("    //TODO: change label\n", replacement)

with open("gnucash/gnome-utils/gnc-recurrence.c", "w") as f:
    f.write(new_content)
