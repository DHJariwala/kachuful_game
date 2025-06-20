from colorama import init, Fore, Style

# initialize colorama (on Windows this enables ANSI codes)
init(autoreset=True)

class KaChuFuL:
    def __init__(self):
        self.player_names = []
        self.current_first_player_index = 0
        self.player_scores = {}
        self.total_hands = 7
        self.current_hand = 7
        self.current_bets = {}
        self.leaderboard = []
        self.hand_order = ["♠️ Kadi", "♦️ Charkat", "♣️ Fali", "♥️ Lal"]
        self.hand_order_index = 0
        self.current_bust_idx = []
        self.current_hand_flow = -1
    def add_players(self):
        n = int(input("Enter number of players: "))
        for i in range(n):
            player_name = input(f"Enter name of player {i + 1}: ")
            self._add_player(player_name)
        print(f"{n} players added.")
    def _add_player(self, player_name):
        if player_name not in self.player_names:
            self.player_names.append(player_name)
            self.player_scores[player_name] = []
            self.current_bets[player_name] = 0
            print(f"Player {player_name} added.")
        else:
            print(f"Player {player_name} already exists.")
    def _set_first_player(self):
        for idx, player in enumerate(self.player_names):
            print(f'{idx}: {player}')
        while True:
            start_idx = input("Enter the number of the player who will go first: ")
            if start_idx.isdigit() and 0 <= int(start_idx) < len(self.player_names):
                break
            else:
                print("Invalid input. Please enter a valid player number.")
        self.set_current_first_player(int(start_idx))
    def set_game(self):
        self._set_first_player()
        n = len(self.player_names)
        print(f"Game set with {n} players.")
        total_possible_handex = 52 // n
        while True:
            total_hands_to_play = int(input(f"Enter total hands to play (default {total_possible_handex}): ") or total_possible_handex)
            if total_hands_to_play <= total_possible_handex:
                self.total_hands = total_hands_to_play
                print(f"Total hands set to {self.total_hands}.")
                break
        self.current_hand = self.total_hands
    def play_game(self):
        print("\nGame started!\n")
        while True:
            self._print_current_hand()
            self.add_hand_order_index()
            self._get_bets()
            self._get_busts()
            self._calculate_scores()
            self._update_leaderboard()
            self._update_first_player()
            self._update_hand()
            continue_game = input("Continue to next hand? (y/n): ").strip().lower()
            if continue_game == 'n':
                print("Game ended.")
                self._print_leaderboard()
                break
        pass
    def _print_current_hand(self):
        # print(f'\nCurrent Hand: {self.hand_order[self.hand_order_index]} ({self.current_hand})\n')
        print(
            f"\n"
            f"{Fore.BLUE}Current Hand: {self.hand_order[self.hand_order_index]} ({self.current_hand})"
            f"\n"
        )
        pass
    def _get_bets(self):
        curr_player_idx = self.current_first_player_index
        cummalative_bet = 0
        for _ in self.player_names:
            player_name = self.player_names[curr_player_idx]
            if self._is_last_player(curr_player_idx):
                if self.current_hand - cummalative_bet < 0:
                    print(f"Last player {player_name} - can bet anything")
                    pass
                else:
                    print(f"Last player {player_name} - cannot bet {self.current_hand - cummalative_bet}.")
            while True:
                bet = input(f"{player_name}, enter your bet for this hand: ")
                if bet.isdigit() and int(bet) >= 0 and int(bet) <= self.current_hand:
                    # If last player, ensure cummalative bet does not equal current total hands
                    if self._is_last_player(curr_player_idx) and cummalative_bet + int(bet) == self.current_hand:
                        print(f"Last player must ensure total bet equals {self.current_hand}. Cannot bet {int(bet)}.")
                        continue
                    self.current_bets[player_name] = int(bet)
                    cummalative_bet += int(bet)
                    break
                else:
                    print("Invalid bet.")
            curr_player_idx = (curr_player_idx + 1) % len(self.player_names)
        print(f"Cummalatieve bet: {cummalative_bet}")
        print()
        pass
    def _is_last_player(self, player_idx):
        return self.current_first_player_index - 1 == player_idx if self.current_first_player_index != 0 else player_idx == len(self.player_names) - 1
    def _get_busts(self):
        self._print_player_idx()
        self.current_bust_idx = list(map(int, input("Enter the indices of players who busted this hand (comma separated): ").split(',')))
        pass
    def _calculate_scores(self):
        for idx, player in enumerate(self.player_names):
            if idx not in self.current_bust_idx:
                self.player_scores[player].append(int('1'+str(self.current_bets[player])))
            else:
                self.player_scores[player].append(0)
        self._print_scores()
    def _print_scores(self):
        print("\nScores:")
        import prettytable as pt
        table = pt.PrettyTable()
        table.field_names = list(self.player_scores.keys())
        for row in zip(*self.player_scores.values()):
            table.add_row(row)
        table.align = "l"
        table.title = "Player Scores"
        print(table)
        pass
    def _update_leaderboard(self):
        total_scores = {player: sum(scores) for player, scores in self.player_scores.items()}
        sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
        self.leaderboard = []
        prev_score = None
        rank = 0

        for player, score in sorted_scores:
            if score != prev_score:
                rank += 1
                prev_score = score
            self.leaderboard.append((rank, player, score))
        self._print_leaderboard()
    def _print_leaderboard(self):
        from prettytable import PrettyTable
        print("\nLeaderboard:")
        table = PrettyTable()
        table.field_names = ["Rank", "Player", "Score"]
        for rank, player, score in self.leaderboard:
            table.add_row([rank, player, score])
        table.align = "l"
        table.title = "Game Leaderboard"
        print(table)
        pass
    def _update_first_player(self):
        self.current_first_player_index += 1
        if self.current_first_player_index >= len(self.player_names):
            self.current_first_player_index = 0
        # print(f"Next first player: {self.player_names[self.current_first_player_index]}")
    def _print_player_idx(self):
        for idx, player in enumerate(self.player_names):
            print(f'{idx}: {player}')
    def _update_hand(self):
        self.current_hand += self.current_hand_flow
        if self.current_hand == 0:
            self.current_hand_flow = 1
            self.current_hand = 1
        elif self.current_hand == self.total_hands:
            self.current_hand_flow = -1
            
    def add_hand_order_index(self):
        self.hand_order_index += 1
        if self.hand_order_index >= len(self.hand_order):
            self.hand_order_index = 0
    def set_current_first_player(self, player_id):
        self.current_first_player_index = player_id
    
        
if __name__ == "__main__":
    # Initialize Game
    game = KaChuFuL()
    # Add players
    game.add_players()
    # Set the game
    game.set_game()
    # Play the game
    game.play_game()
    
    
    