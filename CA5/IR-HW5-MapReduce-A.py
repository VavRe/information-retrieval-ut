from mrjob.job import MRJob
from mrjob.step import MRStep



class MostCommentedVariant(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_extract_variation,
                combiner=self.variant_combiner
            ),
            MRStep(
                reducer=self.reducer_inter
            ),
            MRStep(
                reducer=self.reducer_sorted
            )
           ]

    def mapper_extract_variation(self, _, line):
        yield  line.split("\t")[2] , 1

    def variant_combiner(self, variant, count):
        yield variant,sum(count)

    def reducer_inter(self, variant, counts):
        yield None,(sum(counts),variant)

    def reducer_sorted(self, _, variant_and_counts):
        sorted_count =  sorted(variant_and_counts, reverse=True)
        yield (sorted_count[0])

if __name__ == '__main__':
    MostCommentedVariant.run()
