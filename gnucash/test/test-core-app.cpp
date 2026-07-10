#include <gtest/gtest.h>
#include <iostream>
#include <sstream>

#include "gnucash-core-app.hpp"

extern bool is_development_version;
extern void gnc_print_unstable_message(void);

class StderrCapture {
public:
    StderrCapture() {
        old_cerr_buf = std::cerr.rdbuf();
        std::cerr.rdbuf(capture_buf.rdbuf());
    }

    ~StderrCapture() {
        std::cerr.rdbuf(old_cerr_buf);
    }

    std::string str() const {
        return capture_buf.str();
    }

private:
    std::streambuf* old_cerr_buf;
    std::stringstream capture_buf;
};

class CoreAppTest : public ::testing::Test {
protected:
    void SetUp() override {
        original_is_dev_version = is_development_version;
    }

    void TearDown() override {
        is_development_version = original_is_dev_version;
    }

    bool original_is_dev_version;
};

TEST_F(CoreAppTest, PrintUnstableMessage_NoOutputWhenNotDev) {
    is_development_version = false;
    StderrCapture capture;

    gnc_print_unstable_message();

    EXPECT_EQ(capture.str(), "");
}

TEST_F(CoreAppTest, PrintUnstableMessage_HasOutputWhenDev) {
    is_development_version = true;
    StderrCapture capture;

    gnc_print_unstable_message();

    std::string output = capture.str();
    EXPECT_FALSE(output.empty());

    // Check for expected strings (or placeholders, because gettext might be uninitialized)
    EXPECT_TRUE(output.find("This is a development version.") != std::string::npos ||
                output.find("may or may not work.") != std::string::npos);
    EXPECT_TRUE(output.find("Report bugs and other problems") != std::string::npos);
}
