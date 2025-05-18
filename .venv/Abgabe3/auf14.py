import itertools
import pandas as pd

def prob_sym(s_sent, s_recv):
    if s_sent == s_recv:
        return 1 - p
    else:
        return p / (r - 1)

symbols = [0, 1, 2]
codes = [[0,0,0], [1,1,1], [2,2,2]]
p = 0.2
r = len(symbols)
priors = [0.6, 0.3, 0.1]

received_words = list(itertools.product(symbols, repeat=3))


#Pr(y empfangen | x gesendet) - vorwaerts
channel_probs = []

for codeword in codes:
    row = []
    for y in received_words:
        prob = 1.0
        for s_sent, s_recv in zip(codeword, y):
            prob *= prob_sym(s_sent, s_recv)
        row.append(prob)
    channel_probs.append(row)


filtered_received = []
filtered_probs = [[] for _ in range(len(codes))]

# channel_probs[0] —  Pr(y | 000)
# channel_probs[1] —  Pr(y | 111)
# channel_probs[2] —  Pr(y | 222)

#exclude words that are fehlerfrei (000,111,222)
for i, word in enumerate(received_words):
    include = [word != code for code in codes]

    # add word if it is not what was sent
    if any(include):
        filtered_received.append(word)
        for j in range(3):  #
            if word != codes[j]:
                filtered_probs[j].append(channel_probs[j][i])

#replace
received_words = filtered_received
channel_probs = filtered_probs

#check if probs=1
total=sum(channel_probs[0])+sum(channel_probs[1])+sum(channel_probs[2])
print(total)

# P(x_i | y) for all y - rueckwaerts
posterior_probs = []

for j in range(len(received_words)):
    # Pr(y | x_i) for fixed y
    likelihoods = [channel_probs[i][j] for i in range(3)]

    # Pr(y)
    evidence = sum(l * p for l, p in zip(likelihoods, priors))

    # Bayes formula for  x_i
    posteriors = [(likelihoods[i] * priors[i]) / evidence if evidence > 0 else 0.0 for i in range(3)]

    posterior_probs.append(posteriors)


# ML-rule: x_i with macx Pr(y | x_i)
ml_table = []
for j in range(len(received_words)):
    likelihoods = [channel_probs[i][j] for i in range(3)]
    decoded_ml = likelihoods.index(max(likelihoods))
    ml_table.append(decoded_ml)

# ME-rule x_i with max Pr(x_i | y)
me_table = []
for posteriors in posterior_probs:
    decoded_me = posteriors.index(max(posteriors))
    me_table.append(decoded_me)

df = pd.DataFrame({
    "received_word": received_words,
    "ML_decoded_as": ml_table,
    "ME_decoded_as": me_table
})

df.to_csv("ml_me_decoding_table.tsv\", index=False)

ml_probs = []
for j in range(len(received_words)):
    ml_probs.append([channel_probs[i][j] for i in range(3)])


dfprobs = pd.DataFrame({
    "received_word": received_words,
    "Pr(y|000)": [p[0] for p in ml_probs],
    "Pr(y|111)": [p[1] for p in ml_probs],
    "Pr(y|222)": [p[2] for p in ml_probs],
    "Pr(000|y)": [p[0] for p in posterior_probs],
    "Pr(111|y)": [p[1] for p in posterior_probs],
    "Pr(222|y)": [p[2] for p in posterior_probs],
})


dfprobs.to_csv("forward_and_backward_probs.tsv", index=False)