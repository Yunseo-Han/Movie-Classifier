import pandas as pd
import os
import glob

#set this to print df
##setting folders and files path
pos_folder = os.path.join(os.getcwd(), "Movie_Reviews", "pos")
pos_files = os.path.join(pos_folder, "*.txt")
neg_folder = os.path.join(os.getcwd(), "Movie_Reviews", "neg")
neg_files = os.path.join(neg_folder, "*.txt")

##getting a list of name for both pos and neg folder
pos_file_names = [os.path.basename(x) for x in glob.glob(pos_files)]
neg_file_names = [os.path.basename(x) for x in glob.glob(neg_files)]
##setting result list
pos_li = []
neg_li = []

##for each file, read the line, then push [filename, output, line] into a list
for file_name in pos_file_names:
    file_path = os.path.join(pos_folder, file_name)
    text_file = open(file_path, "r")
    data = text_file.read()
    pos_li.append([file_name[2:-4], 1, data])
    text_file.close()

##for each file, read the line, then push [filename, output, line] into a list
for file_name in neg_file_names:
    file_path = os.path.join(neg_folder, file_name)
    text_file = open(file_path, "r")
    data = text_file.read()
    neg_li.append([file_name[2:-4], 0, data])
    text_file.close()

##use the list to create dataframe
pos_df = pd.DataFrame(pos_li, columns=['id', 'sentiment', 'review'])
neg_df = pd.DataFrame(neg_li, columns=['id', 'sentiment', 'review'])

##split pos/neg dataframe to 1:9, 1 for validation, 9 for training
pos_val = pos_df.sample(frac=0.1)
pos_train = pos_df.drop(pos_val.index)
neg_val = neg_df.sample(frac=0.1)
neg_train = neg_df.drop(neg_val.index)

##merge pos and neg for validation = val_df, training = train_df
val_df = pd.concat([pos_val, neg_val])
train_df = pd.concat([pos_train, neg_train])

##write these into file
val_df.to_csv("val.csv", index=False)
train_df.to_csv("train.csv", index=False)

##validation
print("val_df has {} rows, {} pos vs {} neg".format(len(val_df), len(val_df.loc[val_df['sentiment'] == 1]), len(val_df.loc[val_df['sentiment'] == 0])))
print("train_df has {} rows, {} pos vs {} neg".format(len(train_df), len(train_df.loc[train_df['sentiment'] == 1]), len(train_df.loc[train_df['sentiment'] == 0])))
print("overlapping row : {}".format(len(val_df.merge(train_df, on='id'))))



# pos_df.to_csv("test", index=False)
# print(len(df))
# frame = pd.concat(li, sort=False, ignore_index=True)
# len(frame.count())
