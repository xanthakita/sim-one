class HiveOrchestrator:
    def __init__(self, field):
        self.field = field
        self.hive_location = self.field.place_hive()  # Place the hive on the field
        self.age = 0  # Days the hive has been alive
        self.queen = None  # The queen bee
        self.bees = []  # List of all bees in the hive
        self.nectar = 0  # Nectar collected
        self.honey = 0  # Honey produced

    def add_bee(self, bee):
        self.bees.append(bee)

    def collect_nectar(self, amount):
        self.nectar += amount

    def produce_honey(self):
        # Convert nectar to honey (e.g., 10 nectar = 1 honey)
        honey_produced = self.nectar // 10
        self.honey += honey_produced
        self.nectar -= honey_produced * 10

    def update(self):
        # Increment hive age
        self.age += 1

        # Produce honey
        self.produce_honey()

        # Update all bees
        for bee in self.bees:
            bee.update()

        # Check if the hive should split (e.g., once a year)
        if self.age % 365 == 0 and len(self.bees) > 50:
            self.split_hive()

    def split_hive(self):
        print("The hive is splitting!")
        # Logic for hive splitting (e.g., create a new hive)

    def __str__(self):
        return (f"Hive Age: {self.age} days\n"
                f"Bees: {len(self.bees)}\n"
                f"Nectar: {self.nectar}\n"
                f"Honey: {self.honey}")
        
class QueenBee:
    def __init__(self, hive):
        self.hive = hive
        self.nectar_collected = 0
        self.lifespan = 1460  # 4 years in simulation days
        self.age = 0

    def collect_nectar(self):
        # Simulate nectar collection (e.g., 1 nectar per day)
        nectar = 1
        self.nectar_collected += nectar
        self.hive.collect_nectar(nectar)

    def lay_eggs(self):
        if self.hive.nectar >= 10:
            print("The queen is laying eggs!")
            self.hive.nectar -= 10
            # Add larvae to the hive (e.g., 5 larvae per batch)
            for _ in range(5):
                self.hive.add_bee(Larva(self.hive))

    def update(self):
        self.age += 1
        if self.age > self.lifespan:
            print("The queen has died!")
            self.hive.queen = None
        else:
            self.collect_nectar()
            self.lay_eggs()
            
class Larva:
    def __init__(self, hive):
        self.hive = hive
        self.age = 0
        self.development_time = 21  # 21 days to develop

    def update(self):
        self.age += 1
        if self.age >= self.development_time:
            # Decide what type of bee to become
            if len([bee for bee in self.hive.bees if isinstance(WorkerBee)]) < 50:
                self.hive.add_bee(WorkerBee(self.hive))
            elif len([bee for bee in self.hive.bees if isinstance(DroneBee)]) < 10:
                self.hive.add_bee(DroneBee(self.hive))
            else:
                self.hive.add_bee(QueenBee(self.hive))
            self.hive.bees.remove(self)
            
