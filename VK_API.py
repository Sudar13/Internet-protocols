import requests
import os

class VK_API:
    def __init__(self, identifier: str, api_token: str) -> None:
        self._request_data = None
        self._api_token = api_token or "Вставить свой access_token"
        
        profile_data = self._fetch_user_profile(identifier)
        
        try:
            self.profile_id = profile_data[0]["id"]
            self.profile_details = profile_data[0]
        except (IndexError, KeyError):
            print("Ошибка при получении данных пользователя")
            raise

    def _fetch_user_profile(self, identifier: str) -> dict:
        return requests.get(
            "https://api.vk.com/method/users.get",
            params={
                "access_token": self._api_token,
                "v": "5.199",
                "user_ids": identifier,
                "name_case": "gen"
            }
        ).json().get("response", [])

    def display_friends_list(self) -> None:
        if not self._request_data:
            self._request_data = self._get_friends_data()
            return self.display_friends_list()
            
        friends = self._request_data.json()["response"]["items"]
        print(f"\nКонтакты {self.profile_details['first_name']} {self.profile_details['last_name']}:\n")
        
        for num, friend in enumerate(friends, 1):
            print(f'{num})\t{friend["first_name"]} {friend["last_name"]} - id: {friend["id"]}')

    def _get_friends_data(self):
        return requests.get(
            "https://api.vk.com/method/friends.get",
            params={
                "access_token": self._api_token,
                "v": "8.131",
                "user_id": self.profile_id,
                "fields": "city",
                "order": "name"
            }
        )


def execute_program():
    token = os.environ.get("VK_tkn")
    user_input = input("Введите ID пользователя или короткую ссылку: ")
    vk_instance = VK_API(user_input, token)
    vk_instance.display_friends_list()


if __name__ == '__main__':
    execute_program()