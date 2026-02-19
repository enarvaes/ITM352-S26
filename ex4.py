#recent_purchases = [36.13, 23.87, 183.53, 22.93, 11.62]

#budget = 150
#total_spent = 0

#for purchase in recent_purchases:
    total_spent += purchase
    if total_spent > budget:
        print(f"This purchase is over budget:", purchase)
    else:
        print(f"This purchase is within budget:", purchase)

def check_budget(purchase, limit):
    if purchase > limit:
        return "Over budget"
    else:
        return "Within budget"
    
check_budget(36.13, 150)
