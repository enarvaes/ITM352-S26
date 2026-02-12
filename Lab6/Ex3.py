import site


def determine_progress1(hits, spins): 
    if spins == 0: 
        return "Get going!"
    hits_spins_ratio = hits / spins 

    if hits_spins_ratio > 0: 
        progress = "On your way!" 
        if hits_spins_ratio >= 0.25: 
            progress = "Almost there!" 
            if hits_spins_ratio >= 0.5: 
                if hits < spins: 
                    progress = "You win!" 
    else: 

        progress = "Get going!" 
        
    return progress

#def test_determine_progress1(progress_function): 
    #assert progress_function(10, 0) == "Get going!", "Test 1 failed" [cite: 36, 37]
    #assert progress_function(1, 10) == "On your way!", "Test 2 failed"
    #assert progress_function(3, 10) == "Almost there!", "Test 3 failed"
    #assert progress_function(6, 10) == "You win!", "Test 4 failed"
    #assert progress_function(10, 10) == "Get going!", "Test 5 failed"
    #print("All tests passed!")

#def test_determine_progress2(hits, spins):
    #if spins == 0: return "Get going!"
    #ratio = hits / spins
    #res = "Get going!"
    #if ratio > 0: res = "On your way!"
    #if ratio >= 0.25: res = "Almost there!"
    #if ratio >= 0.5: res = "You win!"
    #if hits >= spins: res = "Get going!"
    #return res

def test_determine_progress3(hits, spins):
    if spins == 0 or hits >= spins:
        return "Get going!"
    ratio = hits / spins
    if ratio >= 0.5:
        return "You win!"
    elif ratio >= 0.25:
        return "Almost there!"
    elif ratio > 0:
        return "On your way!"
    return "Get going!"