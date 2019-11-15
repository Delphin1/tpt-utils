"""
Module uses Teradata Parallel Transporter aka TPT to loading and exporting of date from/to Teradata database.
https://docs.teradata.com/reader/xEzC_kfDJe9nZZ6GRLPvHw/root

Module needs tbuild utility from tptbase,
download from tereadata website https://downloads.teradata.com/download/tools/teradata-tools-and-utilities-linux-installation-package-0
"""

import logging
import os
import subprocess


class Tpt:

    def __init__(self, user, password, host, \
                 templates_dir='templates', max_session=4, charset='UTF8', log_level='DEBUG'):
        logging.basicConfig(level=logging.getLevelName(log_level))
        self.exec_template = """var_tdpid='{}', var_userid='{}',  var_password='{}', var_maxsessions={}, var_utf='{}', var_dateform='ANSIDATE', var_format='DELIMITED',""" \
            .format(host, user, password, max_session, charset)
        self.templates_dir = templates_dir
        self.max_session = max_session

    def file_to_teradata(self, file, table, delimeter='|', template='import.tpt'):
        """Load data from file to teradata table"""
        exec_str = "tbuild -f {} -u ".format(self.templates_dir + '/' + template) + '"' + self.exec_template + \
        """var_directorypath='{}', var_inputfile='{}', var_tablename='{}',  var_delimiter_value='{}' """.format(os.path.dirname(file), os.path.basename(file), table, delimeter) + '"'
        logging.debug("exec_str: {}".format(exec_str))
        exit_code = subprocess.call(exec_str, shell=True)
        if exit_code != 0 :
            logging.error("Something went wrong!\n Use command for view log: tlogview -j [jobid] ")
        else:
            logging.info("File {} saved.".format(file))
        return exit_code

    def _convert_decimal_point(self, file, fr, to):
        """Convert decimal point for float numbers"""
        sed_str = """sed -i '/[0-9]\{0}/s/\{0}/{1}/g' {2}""".format(fr, to, file)
        logging.debug("sed_str: " + sed_str)
        exit_code = subprocess.call(sed_str, shell=True)
        return exit_code

    def teradata_to_file(self, query, file, delimeter='|', template='export.tpt'):
        """Save data from sql query to file with delimeter"""
        exec_str = "tbuild -f {} -u ".format(self.templates_dir + '/' + template) + '"' + self.exec_template + \
        """var_delimiter_value='{}', var_exportquery='{}', var_directorypath='{}', var_outfile='{}'""" \
            .format(delimeter, query.replace("'", "''") + ';', os.path.dirname(file), os.path.basename(file)) + '"'
        logging.debug("exec_str: {}".format(exec_str))
        exit_code = subprocess.call(exec_str, shell=True)
        logging.debug("exit_code: " + str(exit_code))
        if exit_code != 0 :
            logging.error("Something went wrong!\n Use command for view log: tlogview -j [jobid] ")
        else:
            self._convert_decimal_point(file, ',', '.')
            logging.info("File {} saved.".format(file))
        return exit_code
