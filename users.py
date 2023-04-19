import logging
import pandas

logging.log(level=logging.INFO)


class UserHandler:

    def __init__(self, chat_id):
        self.user = int(chat_id)
        self.csvfile = 'users.csv'  # better create config with this data
        self.users_df = pandas.read_csv(self.csvfile, index_col="id")
        self.users_df = self.users_df.applymap(lambda x: x if type(x) is str else None)

    def __no_user_error(self):
        logging.warning(f"No user {self.user} in Users DB")
        return None

    def __write_to_cvs(self, df):
        logging.info("Important: Changing Users DB")
        df.to_csv(self.csvfile)

    def check_for_user(self):
        if self.user in self.users_df.index:
            return True
        else:
            return False

    def add_user(self):
        if not self.check_for_user():
            new_df = pandas.DataFrame({"city": None, "subscription": None},
                                      index=[self.user])
            new_df.index.name = 'id'
            logging.info(f"Adding new user {self.user} in DB")
            self.__write_to_cvs(pandas.concat([self.users_df, new_df]))
        else:
            print('User already exist')

    def delete_user(self):
        if self.check_for_user():
            df = self.users_df.drop([self.user])
            logging.info(f"Deleting user {self.user} from DB")
            self.__write_to_cvs(df)
        else:
            self.__no_user_error()

    def update_user(self, city, subscription):
        if self.check_for_user():
            new_df = self.users_df.copy()
            new_df.at[self.user, 'city'] = city
            new_df.at[self.user, 'subscription'] = subscription
            logging.info(f"Updating user {self.user} in DB with data > city: {city}, subscr:{subscription}")
            self.__write_to_cvs(new_df)
        else:
            self.__no_user_error()

    def get_users_city(self):
        if self.check_for_user():
            return self.users_df.loc[self.user]['city']
        else:
            return self.__no_user_error()

    def get_users_subscription(self):
        if self.check_for_user():
            return self.users_df.loc[self.user]['subscription']
        else:
            return self.__no_user_error()
