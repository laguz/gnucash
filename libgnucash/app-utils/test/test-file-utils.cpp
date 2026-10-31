/********************************************************************\
 * test-file-utils.cpp -- tests for file-utils.c                    *
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
 *                                                                  *
\********************************************************************/

#include <config.h>
#include <glib.h>
#include <glib/gstdio.h>
#include <string>
#include <cstdio>

#include "file-utils.h"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wcpp"
#include <gtest/gtest.h>
#pragma GCC diagnostic pop

class FileUtilsTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        gchar *tmp_dir = g_dir_make_tmp("gnc_test_file_utils_XXXXXX", nullptr);
        ASSERT_NE(tmp_dir, nullptr);
        m_temp_dir = tmp_dir;
        g_free(tmp_dir);
    }

    void TearDown() override
    {
        if (!m_temp_dir.empty())
        {
            GDir *dir = g_dir_open(m_temp_dir.c_str(), 0, nullptr);
            if (dir)
            {
                const gchar *entry;
                while ((entry = g_dir_read_name(dir)) != nullptr)
                {
                    gchar *filepath = g_build_filename(m_temp_dir.c_str(), entry, nullptr);
                    g_unlink(filepath);
                    g_free(filepath);
                }
                g_dir_close(dir);
            }
            g_rmdir(m_temp_dir.c_str());
        }
    }

    std::string create_temp_file(const std::string &basename, const std::string &content)
    {
        gchar *filepath = g_build_filename(m_temp_dir.c_str(), basename.c_str(), nullptr);
        std::string path_str = filepath;
        g_free(filepath);

        FILE *fp = g_fopen(path_str.c_str(), "wb");
        if (fp)
        {
            if (!content.empty())
            {
                fwrite(content.data(), 1, content.size(), fp);
            }
            fclose(fp);
        }
        return path_str;
    }

    std::string m_temp_dir;
};

/* Test gncReadFile with invalid parameters (NULL / empty string) */
TEST_F(FileUtilsTest, ReadFileInvalidFilename)
{
    char *data = reinterpret_cast<char *>(0x1234);
    int size = gncReadFile(nullptr, &data);
    EXPECT_EQ(size, 0);

    data = reinterpret_cast<char *>(0x1234);
    size = gncReadFile("", &data);
    EXPECT_EQ(size, 0);
}

/* Test gncReadFile when file does not exist */
TEST_F(FileUtilsTest, ReadFileNonExistent)
{
    gchar *fake_path = g_build_filename(m_temp_dir.c_str(), "nonexistent_file.txt", nullptr);
    char *data = nullptr;

    g_test_expect_message("gnc.app-utils", G_LOG_LEVEL_CRITICAL, "*No such file or directory*");
    int size = gncReadFile(fake_path, &data);
    EXPECT_EQ(size, 0);
    EXPECT_EQ(data, nullptr);
    g_test_assert_expected_messages();

    g_free(fake_path);
}

/* Test gncReadFile on an empty file */
TEST_F(FileUtilsTest, ReadFileEmpty)
{
    std::string path = create_temp_file("empty.txt", "");
    char *data = nullptr;

    int size = gncReadFile(path.c_str(), &data);
    EXPECT_EQ(size, 0);
    ASSERT_NE(data, nullptr);
    EXPECT_STREQ(data, "");
    EXPECT_EQ(data[0], '\0');

    g_free(data);
}

/* Test gncReadFile with regular small content */
TEST_F(FileUtilsTest, ReadFileSmallContent)
{
    std::string content = "<html><body>Hello, GnuCash!</body></html>";
    std::string path = create_temp_file("test.html", content);
    char *data = nullptr;

    int size = gncReadFile(path.c_str(), &data);
    EXPECT_EQ(size, static_cast<int>(content.size()));
    ASSERT_NE(data, nullptr);
    EXPECT_STREQ(data, content.c_str());

    g_free(data);
}

/* Test gncReadFile with multi-line content */
TEST_F(FileUtilsTest, ReadFileMultiLine)
{
    std::string content = "Line 1: GnuCash\nLine 2: Accounting\nLine 3: Open Source\n";
    std::string path = create_temp_file("multiline.txt", content);
    char *data = nullptr;

    int size = gncReadFile(path.c_str(), &data);
    EXPECT_EQ(size, static_cast<int>(content.size()));
    ASSERT_NE(data, nullptr);
    EXPECT_STREQ(data, content.c_str());

    g_free(data);
}

/* Test gncReadFile with larger content (~64 KB) */
TEST_F(FileUtilsTest, ReadFileLargeContent)
{
    std::string content;
    content.reserve(65536);
    for (int i = 0; i < 2048; ++i)
    {
        content.append("0123456789ABCDEF0123456789ABCDEF\n");
    }

    std::string path = create_temp_file("large.txt", content);
    char *data = nullptr;

    int size = gncReadFile(path.c_str(), &data);
    EXPECT_EQ(size, static_cast<int>(content.size()));
    ASSERT_NE(data, nullptr);
    EXPECT_EQ(std::string(data, size), content);

    g_free(data);
}

/* Test gncReadFile with embedded null bytes */
TEST_F(FileUtilsTest, ReadFileBinaryContent)
{
    std::string content = std::string("pre\0post\0end", 12);
    std::string path = create_temp_file("binary.bin", content);
    char *data = nullptr;

    int size = gncReadFile(path.c_str(), &data);
    EXPECT_EQ(size, 12);
    ASSERT_NE(data, nullptr);
    EXPECT_EQ(memcmp(data, content.data(), 12), 0);
    EXPECT_EQ(data[12], '\0');

    g_free(data);
}

/* Test gnc_getline with single and multiple lines */
TEST_F(FileUtilsTest, GetlineBasic)
{
    std::string content = "First line\nSecond line\nThird line without newline";
    std::string path = create_temp_file("getline.txt", content);

    FILE *fp = g_fopen(path.c_str(), "r");
    ASSERT_NE(fp, nullptr);

    gchar *line = nullptr;
    gint64 len = gnc_getline(&line, fp);
    EXPECT_EQ(len, 11);
    ASSERT_NE(line, nullptr);
    EXPECT_STREQ(line, "First line\n");
    g_free(line);
    line = nullptr;

    len = gnc_getline(&line, fp);
    EXPECT_EQ(len, 12);
    ASSERT_NE(line, nullptr);
    EXPECT_STREQ(line, "Second line\n");
    g_free(line);
    line = nullptr;

    len = gnc_getline(&line, fp);
    EXPECT_EQ(len, 26);
    ASSERT_NE(line, nullptr);
    EXPECT_STREQ(line, "Third line without newline");
    g_free(line);
    line = nullptr;

    len = gnc_getline(&line, fp);
    EXPECT_EQ(len, 0);
    ASSERT_NE(line, nullptr);
    EXPECT_STREQ(line, "");
    g_free(line);

    fclose(fp);
}
