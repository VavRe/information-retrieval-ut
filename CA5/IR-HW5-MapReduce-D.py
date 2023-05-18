from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime


class MRWordFrequencyCount(MRJob):
     
    
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                combiner= self.combiner,
                # reducer=self.reducer
            ),
            # MRStep(
                # reducer=self.reducer_sorted
            # )
           ]


    def mapper(self, _, line):

        point = line.split("\t")[0]

        if point.isdigit() and  int(point) == 1:

               yield line.split("\t")[2],(line.split("\t")[1],1) 

    def combiner(self, variant, data):   #bigram & counts are from yield returns from mapper
        countss = 0
        dates = []
        for date, count in data:
            countss += 1
            dates.append(date)
        yield variant,(countss,dates)
    
    # def reducer_sorted(self, _, values):
        
    #     for count,dates in values:
            
    #     yield(x[0])
    # def reducer(self, variant, counts): #bigram & counts are from yield returns from combiner
    #     yield None,(sum(counts),variant)




if __name__ == '__main__':
    MRWordFrequencyCount.run()
