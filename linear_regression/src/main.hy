(import [numpy :as np]
        [matplotlib [pyplot :as plt]]
        [seaborn :as sns]
        [pandas :as pd]
        [sklearn.preprocessing [OrdinalEncoder]]
        [sklearn.model_selection [train_test_split]]
        [sklearn.linear_model [LinearRegression]]
)

(defn split_data [data]
    [(data.drop "score" :axis 1) data.score])

(defn plot_value_count_chart[data column type] 
    (setv figure (plt.figure :figsize [7 7]))
    (plt.title "Agent type counts")
    (.plot :kind type :cmap "viridis" (.value_counts(get data column)))
    (plt.xticks :rotation 0)
    (plt.show)
)

(defn plot_time_score_pairplot[data]
    (setv figure (sns.pairplot data :hue "is_win" :diag_kind "hist" :height 4))
    (figure.fig.suptitle "Time vs score")
    (figure.fig.set_size_inches [7 7])
    (plt.show)
)

;; Load the data
(setv data (pd.read_csv "data/records.csv" ))
(print "Dataset")
(print (data.head))

;; Split the data into train and test
(setv test_data
(cut data 0 5))
(setv train_data (cut data 5 (len data)))

;; EDA
(plot_value_count_chart train_data "agent_type" "bar")
(plot_time_score_pairplot train_data)

;; Split the data into x and y
(setv x (get (split_data train_data) 0))
(setv y (get (split_data train_data) 1))

;;Split the data into train and validation
(setv split (train_test_split x y :test_size 0.2 :shuffle True))
(setv x_train (get split 0))
(setv x_valid (get split 1))
(setv y_train (get split 2))
(setv y_valid (get split 3))

;; Encode categorical variables
(setv cat_cols ["is_win" "agent_type"])
(setv encoder (OrdinalEncoder))
(assoc x_train cat_cols (encoder.fit_transform (get x_train cat_cols)))
(assoc x_valid cat_cols (encoder.transform (get x_valid cat_cols)))

;;Regression model
(setv model (LinearRegression))
(model.fit x_train y_train)
(print "Regression coefficients:")
(print model.coef_)
(print (+ "R2 score:" (str (model.score x_valid  y_valid))))

;;Prediction
(setv x_test (get (split_data test_data) 0))
(setv y_test (get (split_data test_data) 1))
(assoc x_test cat_cols (encoder.transform (get x_test cat_cols)))
(setv y_pred (model.predict x_test))
(print "Predicted values:")
(print y_pred)

;;Compute statistics 
(setv stats (pd.DataFrame {
    "Y_true-Y_pred" (np.abs (- y_test y_pred))
    "Y_true-Y_mean" (np.abs(- y_test (y_train.mean)))
 }))

(print stats)



