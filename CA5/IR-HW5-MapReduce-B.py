from mrjob.job import MRJob
from mrjob.step import MRStep



class MRHighestAvgPoints(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_extract_variation_points,
                reducer=self.reducer_variation_points_avg
            ),
           MRStep(
                reducer=self.reducer_inter
            ),
            MRStep(
                reducer=self.reducer_sorted
            )
           ]

    def mapper_extract_variation_points(self, _, line):
        if line.split("\t")[0].isdigit():
            yield  line.split("\t")[2] , (int(line.split("\t")[0])) 

    def reducer_variation_points_avg(self, variant, points):
        sum_ = 0 
        count_ = 0
        for point in points:
            sum_ += point
            count_ += 1
        
        yield variant,(sum_/count_)

    def reducer_inter(self, variant, avg_point):
        yield None,(sum(avg_point),variant)

    def reducer_sorted(self, _, variant_and_avg_points):
        data_sorted =  sorted(variant_and_avg_points, reverse=True)
        for i in range(5):
            yield(data_sorted[i])


if __name__ == '__main__':
    MRHighestAvgPoints.run()
