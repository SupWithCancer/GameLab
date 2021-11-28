(import [pandas :as pd])
(import [numpy :as np])

(setv path "data/records.csv")
(setv data (pd.read_csv path))

(setv score (get data "score"))
(setv mean_score ( / (.sum score) (len score)))
(setv mean_score_sq ( / (.sum (.pow score 2)) (len score)))
(setv variance (np.sqrt ( - (** mean_score 2) mean_score_sq)))
(print "Score variance:" (.var score))

(setv time (get data "time"))
(print "Time mean:" ( / (.sum time) (len time)))