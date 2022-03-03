import traceback

import htmlmin
import sys
import os
import re
import shutil
import subprocess

remove_empty_space = re.compile(r"\s{2,}").sub
yui_compilation_css = 'java -jar {compiler_path} {input_file} -o {output_file} '
closure_compilation_javascript = 'java -jar {compiler_path}  ' \
                                 '--compilation_level {compilation_level} ' \
                                 '--js {file_name} --js_output_file {output_file} --strict_mode_input=false'


def minify_html(input_file: str, remove_all_space: bool = True) -> None:
    with open(input_file, "r", encoding="utf-8") as input_stream:
        html = htmlmin.minify(input_stream.read(), remove_comments=True, remove_empty_space=True)
    if remove_all_space:
        html = remove_empty_space(" ", html)
    with open(input_file, "w", encoding="utf-8") as output_stream:
        output_stream.write(html)


def minify_javascript(input_file: str, use_java: bool = True) -> None:
    compilation_levels = ["ADVANCED_OPTIMIZATIONS", "SIMPLE_OPTIMIZATIONS"]
    helper_file = "_____helper.js"
    if use_java:
        with open(os.devnull, 'wb') as devnull:
            compilation_list = closure_compilation_javascript.format(
                compiler_path="closure_jars/closure-compiler-v20200719.jar",
                compilation_level=compilation_levels[1],
                file_name=input_file,
                output_file=helper_file).split()
            subprocess.check_call(compilation_list, stdout=devnull, stderr=subprocess.STDOUT)

        shutil.copy2(helper_file, input_file)
        os.remove(helper_file)


def minify_css(input_file: str, use_java: bool = True) -> None:
    helper_file = "_____helper.css"
    if use_java:
        with open(os.devnull, 'wb') as devnull:
            compilation_list = yui_compilation_css.format(
                compiler_path="closure_jars/yuicompressor-2.4.7.jar",
                input_file=input_file,
                output_file=helper_file).split()
            subprocess.check_call(compilation_list, stdout=devnull, stderr=subprocess.STDOUT)

        shutil.copy2(helper_file, input_file)
        os.remove(helper_file)


def process_html(input_directory, debug=False):
    for file_name in os.listdir(input_directory):
        whole_file_path = os.path.join(input_directory, file_name)
        if os.path.isdir(whole_file_path):
            process_html(whole_file_path)
        else:
            try:
                if file_name.endswith(".html"):
                    minify_html(whole_file_path)
                elif file_name.endswith(".js"):
                    minify_javascript(whole_file_path)
                elif file_name.endswith(".css"):
                    minify_css(whole_file_path)
                else:
                    continue
                print("File: " + whole_file_path + " has been minified!")
            except:
                print("Can't minify file: " + whole_file_path)
                if debug:
                    print(traceback.print_exc())


if __name__ == "__main__":
    process_html(sys.argv[1])
