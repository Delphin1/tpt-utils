"""
Module uses Teradata Parallel Transporter aka TPT to loading and exporting of date from/to Teradata database.
https://docs.teradata.com/reader/xEzC_kfDJe9nZZ6GRLPvHw/root

Module needs tbuild utility from tptbase,
download from tereadata website https://downloads.teradata.com/download/tools/teradata-tools-and-utilities-linux-installation-package-0
"""

import logging
import os
import subprocess

class TPT:
    def __init__(self, user, password, host, templates_dir='templates', max_session=4, log_level='DEBUG'):
        logging.setLevel(logging.getLevelName(log_level))
        self.user = user
        self.password = password
        self.host = host
        self.templates_dir = templates_dir
        self.max_session = max_session

    def file_to_teradata(self, file, table, delimeter='|', template='import.tpt'):
        """Load data from file to teradata table"""
        pass

    def teradata_to_file(self, query, file, delimeter='|', template='export.tpt'):
        """Save data from sql query to file with delimeter"""
        exec_str = """
        tbuild - f {0} - u
        var_tdpid='{1}',
        var_userid='{2}',
        var_password='{3}',
        var_exportquery='{4}'' ,
        var_directorypath='{5}',
        var_outfile='{6}',
        var_delimiter_value='{7}',
        var_utf='UTF8',
        var_maxsessions={8},
        var_dateform='ANSIDATE'
        var_format='DELIMITED'""".format(os.path.join(self.templates_dir, template),
                                         self.host,
                                         self.user,
                                         self.host,
                                         query,
                                         os.path.dirname(file),
                                         os.path.basename(file),
                                         delimeter,
                                         self.max_session)
        logging.debug("exec_str: {}".format(exec_str))
        exit_code = subprocess.call(exec_str, shell=True)
        logging.debug("exit_code: " + str(exit_code))
        if exit_code !=0:
            logging.error("Something went wrong!\n Use command for view log: tlogview -j [jobid] ")
        else:
            logging.info("File {} saved.".format(file))
