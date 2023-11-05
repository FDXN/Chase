import random
import numpy as np

class Attributes():
    def __init__(self):
        self.soul_root = {
                            "Metal": 0,
                            "Wood": 0,
                            "Water": 0,
                            "Fire": 0,
                            "Earth": 0,
                            "Gene": 0,
                            "Pure": 0
                          }
    
    def generate_random_array(self, required=5, max=100, weighted=10):
        # 生成随机数组
        sum_numbers = -1
        while sum_numbers != max:
            # 平均分布生成required个随机数
            random_numbers = [random.randint(0,max) for _ in range(required)]

            # 生成权重
            weighted_number = np.clip(np.random.exponential(scale=1/weighted), 0, 2) * max
            
            # 为随机一个位置加上权重
            random_index = random.randint(0, required-1)
            # weighted_number = 100
            random_numbers[random_index] += weighted_number
            
            # 计算总和
            total_sum = np.sum(random_numbers)
            
            # 归一化，使总和为100
            normalized_numbers = np.round((random_numbers / total_sum) * max).astype(int)
            
            sum_numbers = np.sum(normalized_numbers)
            
        normalized_numbers = [int(x) for x in normalized_numbers] 
            
        return normalized_numbers

    def generate(self, required=5, max=100, weighted=10):
        # 直接生成属性
        
        random_array = self.generate_random_array(required, max, weighted)
        
        for element, value in zip(self.soul_root.keys(), random_array):
            self.soul_root[element] = value
        self.soul_root["Gene"] = weighted
        self.soul_root["Pure"] = self.pure()
        return self.soul_root
    
    def inherit(self, father, mother, inherit_num=2):
        # 通过继承生成属性
        self.soul_root = {
                            "Metal": 0,
                            "Wood": 0,
                            "Water": 0,
                            "Fire": 0,
                            "Earth": 0,
                            "Gene": 0,
                            "Pure": 0
                          }
        # 先随机生成一个数据
        
        def mutate(father, mother, mutation_rate=0.1, mutation_magnitude=0.5):
            child = (father+mother)/2
            if random.random() < mutation_rate:
                mutation = random.uniform(-2*mutation_magnitude, mutation_magnitude)
                child += mutation
            return child
        
        random_keys = random.sample(list(self.soul_root.keys())[:5], inherit_num)
        # 随机指定保留的数据，并替换
        for key in random_keys:
            self.soul_root[key] = random.choice([father.soul_root[key], mother.soul_root[key]])
        
        # 继承父母中较低的权重
        self.soul_root["Gene"] = mutate(father.soul_root["Gene"], mother.soul_root["Gene"])
        weighted = self.soul_root["Gene"]
        
        # 计算当前和并生成自己的数值
        current_sum = max(self.soul_root[key] for key in list(self.soul_root.keys())[:5])
        replenish = self.generate_random_array(required=5-inherit_num, max=100-current_sum, weighted=weighted)
        
        # 替换未继承数值
        for key in self.soul_root.keys():
            if key not in random_keys:
                if len(replenish) > 0:
                    self.soul_root[key] = replenish[0]
                    # 如果属性没有继承，则随机生成一个值填入
                    replenish = np.delete(replenish, 0)
                else:
                    break
        
        self.soul_root["Pure"] = self.pure()
        return self.soul_root

    def pure(self):
        return round(sum((key/100) ** 2 for key in list(self.soul_root.values())[:5]), 4)