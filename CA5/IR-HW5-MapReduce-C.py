from mrjob.job import MRJob
from mrjob.step import MRStep
import re

FINDING_WORDS_REGEX = re.compile(r'\b\w+\b')


class MRBigramMostCount(MRJob):
     
    
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                combiner= self.combiner ,
                reducer=self.reducer
            ),
            MRStep(
                reducer=self.reducer_sorted
            )
           ]


    def mapper(self, _, line):

        point = line.split("\t")[0]
        if point.isdigit() and ( int(point) == 4 or int(point) == 5):

            words = FINDING_WORDS_REGEX.findall(line.split("\t")[3])
            for i in range(len(words)-1):
                yield(words[i].lower() + ' ' + words[i+1].lower(), 1)

    def combiner(self, bigram, counts):  
        yield (bigram, sum(counts))

    def reducer(self, bigram, counts): 
        yield None,(sum(counts),bigram)

    def reducer_sorted(self, _, counts):
        x =  sorted(counts, reverse=True)
        # yield(x[0])
        for i in range(5):
            yield(x[i])



if __name__ == '__main__':
    MRBigramMostCount.run()
