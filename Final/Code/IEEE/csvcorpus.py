from __future__ import with_statement

import logging
import csv
import itertools

from gensim import interfaces, utils

logger = logging.getLogger('gensim.corpora.csvcorpus')


class CsvCorpus(interfaces.CorpusABC):
    """
    Corpus in CSV format. The CSV delimiter, headers etc. are guessed automatically
    based on the file content.
    All row values are expected to be ints/floats.
    """

    def __init__(self, fname, labels):
        """
        Initialize the corpus from a file.
        `labels` = are class labels present in the input file? => skip the first column
        """
        logger.info("loading corpus from %s" % fname)
        self.fname = fname
        self.length = None
        self.labels = labels

        # load the first few lines, to guess the CSV dialect
        head = ''.join(itertools.islice(utils.smart_open(self.fname), 5))
        self.headers = csv.Sniffer().has_header(head)
        self.dialect = csv.Sniffer().sniff(head)
        logger.info("sniffed CSV delimiter=%r, headers=%s" % (self.dialect.delimiter, self.headers))

    def __iter__(self):
        """
        Iterate over the corpus, returning one sparse vector at a time.
        """
        reader = csv.reader(utils.smart_open(self.fname), self.dialect)
        if self.headers:
            next(reader)    # skip the headers

        line_no = -1
        for line_no, line in enumerate(reader):
            # if self.labels:
            #     line.pop(0)  # ignore the first column = class label
            yield list(enumerate(line))

        self.length = line_no + 1  # store the total number of CSV rows = documents
