import json
import csv
import webbrowser
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")

# Define values
words = {}
scores = []
scoreList = []
validWords = []
TEST_SIZE = 20
currentSize = 0


def trainData(reviewList, newWords):
    """ Check words in review and assign score """
    for review in reviewList:
        reviewText, reviewScore = review
        reviewText = [word for word in reviewText.split() if word in validWords]

        if reviewScore > 2:
            point = 1
        else:
            point = -1

        # Assign words
        for word in reviewText:
            try:
                newWords[word] += point
            except Exception:
                newWords[word] = point
    return newWords


def testData(reviewList, newWords):
    """ Test review with saved data """
    totalScore = 0
    for review in reviewList:
        points = 0
        reviewText, reviewScore = review
        reviewText = [word for word in reviewText.split() if word in validWords]

        if reviewScore > 2:
            point = 1
        else:
            point = -1

        for word in reviewText:
            try:
                # If word exists
                points += newWords[word]
            except Exception:
                newWords[word] = point

        # Check whether it predicted correct
        totalScore += int((reviewScore > 2 and points >= 0) or (reviewScore < 3 and points < 0))

    return newWords, totalScore/len(reviewList)


# Open files
with open("data/amazon_reviews.json") as f:
    reviewData = json.load(f)

with open("data/adjectives_in_english_language.json") as f:
    data = json.load(f)
    validWords += data

with open("data/adverbs_in_english_language.json") as f:
    data = json.load(f)
    validWords += data

with open("data/fillerWords.json") as f:
    data = json.load(f)
    validWords = [word for word in validWords if word not in data]


# Train initial set
trainWords = reviewData[:TEST_SIZE]
del reviewData[:TEST_SIZE]
words = trainData(trainWords, words)
currentSize += 20

# Test data in parts and learn
for _ in range(len(reviewData) // TEST_SIZE):
    trainWords = reviewData[:TEST_SIZE]
    del reviewData[:TEST_SIZE]

    words, score = testData(trainWords, words)
    currentSize += TEST_SIZE

    if scoreList:
        # Calculate average accuracy
        average = round(sum(scoreList) / len(scoreList), 3)
        scoreList.append(score)

    else:
        average = score
        scoreList.append(score)

    scores.append((currentSize, average))

# Sort dict
words = dict(sorted(words.items(), key=lambda item: item[1]))

# Output data in a CSV file
with open("wordData.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    for record in reversed(list(map(list, words.items()))):
        writer.writerow(record)

webbrowser.open("wordData.csv")

x = [item[0] for item in scores]
y = [item[1] for item in scores]

# Generate graph
plt.plot(x, y, color="green", marker="o")
plt.title("Amazon Review Learner", fontsize=14)
plt.xlabel("No. of reviews Tested")
plt.ylabel("Accuracy")
plt.show()
