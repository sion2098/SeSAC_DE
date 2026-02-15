# Flink 클러스터에 제출할 Word Count Job
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.common import Types

env = StreamExecutionEnvironment.get_execution_environment()
env.set_runtime_mode(RuntimeExecutionMode.BATCH)
env.set_parallelism(1)

word_count_data = [
    "To be, or not to be,--that is the question:--",
    "Whether 'tis nobler in the mind to suffer",
    "The slings and arrows of outrageous fortune",
    "Or to take arms against a sea of troubles,"
]

def split(line):
    yield from line.split()

ds = env.from_collection(word_count_data)
result = ds.flat_map(split) \
           .map(lambda word: (word, 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()])) \
           .key_by(lambda x: x[0]) \
           .reduce(lambda a, b: (a[0], a[1] + b[1]))

# .key_by(lambda x: x[0]) : 같은 키를 가진 데이터가 같은 파티션(같은 태스크/노드)로 가도록 재분배
# reduce는 같은 키끼리만 계산해야 함(key_by 없으면 같은 키인데 다른 노드에 흩어져서 정확한 합산 불가능)
# 현재는 set_parallelism(1)이라 사실상 한 노드만 쓰기 때문에 key_by 효과가 눈에 안 보임
result.print()
env.execute("Word Count Job - Cluster")
