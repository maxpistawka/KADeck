from supermemo2 import SMTwo


import hgtk

decomposed = hgtk.letter.decompose("않")
consonants = {""}

print(decomposed)

# first review
# using quality=4 as an example, read below for what each value from 0 to 5 represents
# review date would default to date.today() if not provided
review = SMTwo.first_review(5, "2021-3-14")
print(review.easiness)
# review prints SMTwo(easiness=2.36, interval=1, repetitions=1, review_date=datetime.date(2021, 3, 15))

# second review
review = SMTwo(review.easiness, review.interval, review.repetitions).review(4, "2021-3-14")
review.review_date
# review prints similar to example above.