from context import lib

from lib.text_util.util import TextUtils

Title = "\"Work Laptop Confiscated: Boss's Secret Plot | AITA Chores Dispute Reignited: Who's Responsible | Reorganizing Daughter's Room: A Parenting Slip | TikTok Tribute Stirring Family Tension: AITA\""
reduced = TextUtils.cut_words(Title, 150)  #194 characters in title
print(reduced)

tags = "AITA,THINGIFYYYYY,SHIT YOUR SELF,  NOW,HE,"
reduced = TextUtils.cut_words(tags, 35, split_around=',')
print(reduced)
