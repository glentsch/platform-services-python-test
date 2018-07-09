#!/usr/bin/env python
from pymongo import MongoClient


def main():
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    print("Removing and reloading rewards in mongo")
    db.rewards.remove()
    db.rewards.insert({"points": 100, "rewardName": "5% off purchase", "tier": "A", "deduction": 0.05})
    db.rewards.insert({"points": 200, "rewardName": "10% off purchase", "tier": "B", "deduction": 0.10})
    db.rewards.insert({"points": 300, "rewardName": "15% off purchase", "tier": "C", "deduction": 0.15})
    db.rewards.insert({"points": 400, "rewardName": "20% off purchase", "tier": "D", "deduction": 0.20})
    db.rewards.insert({"points": 500, "rewardName": "25% off purchase", "tier": "E", "deduction": 0.25})
    db.rewards.insert({"points": 600, "rewardName": "30% off purchase", "tier": "F", "deduction": 0.30})
    db.rewards.insert({"points": 700, "rewardName": "35% off purchase", "tier": "G", "deduction": 0.35})
    db.rewards.insert({"points": 800, "rewardName": "40% off purchase", "tier": "H", "deduction": 0.40})
    db.rewards.insert({"points": 900, "rewardName": "45% off purchase", "tier": "I", "deduction": 0.45})
    db.rewards.insert({"points": 1000, "rewardName": "50% off purchase", "tier": "J", "deduction": 0.50})
    print("Rewards loaded in mongo")

if __name__ == "__main__":
    main()