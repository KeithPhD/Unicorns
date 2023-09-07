#!/usr/bin/env python
# coding: utf-8

# In[187]:


import random
import pygame
import pygame.freetype
import sys
import os
import time
os.chdir(r'C:\Users\Keith\New folder\Card Games\Card Images')


# In[188]:


class UnoCard:
    def __init__(self, name, typing):
        self.name = name
        self.typing = typing
        self.image = pygame.image.load(self.name + ".png")

    def __str__(self):
        return f"{self.name} ({self.typing})"


# In[189]:


class UnoDeck:
    def __init__(self): # Skipped: Ginormous Unicorn, Swift Flying Unicorn, Yay, Nanny Cam, Slowdown
        names_typings = [("Basic Unicorn", "Basic")] * 15 + [("Sadistic Ritual", "Downgrade")] + [("Pandamonium", "Downgrade")] + [("Broken Stable", "Downgrade")] + [("Unicorn Poison", "Magic Card")] + [("Blinding Light", "Downgrade")] + [("Magical Kittencorn", "Magical Unicorn")] + [("Stable Artillery", "Upgrade")] + [("Rainbow Lasso", "Upgrade")] + [("Rainbow Aura", "Upgrade")] + [("Double Dutch", "Upgrade")] + [("Glitter Bomb", "Upgrade")] + [("Targeted Destruction", "Magic Card")] + [("Shake up", "Magic Card")] + [("Two-For-One", "Magic Card")] + [("Re-Target", "Magic Card")] + [("Reset Button", "Magic Card")] + [("Mystical Vortex", "Magic Card")] + [("Good Deal", "Magic Card")] + [("Kiss of Life", "Magic Card")] + [("Change of Luck", "Magic Card")] + [("Glitter Tornado", "Magic Card")] + [("Caffeine Overload", "Upgrade")] + [("Claw Machine", "Upgrade")] + [("Rhinocorn", "Magical Unicorn")] + [("Blatant Thievery", "Magic Card")] + [("Back Kick", "Magic Card")] + [("Unicorn Phoenix", "Magical Unicorn")] + [("Unicorn Oracle", "Magical Unicorn")] + [("Unicorn on the Cob", "Magical Unicorn")] + [("The Great Narwhal", "Magical Unicorn")] + [("Shark With a Horn", "Magical Unicorn")] + [("Shabby the Narwhal", "Magical Unicorn")] + [("Seductive Unicorn", "Magical Unicorn")] + [("Narwhal Torpedo", "Magical Unicorn")] + [("Mermaid Unicorn", "Magical Unicorn")] + [("Mother Goose Unicorn", "Magical Unicorn")] + [("Majestic Flying Unicorn", "Magical Unicorn")] + [("Magical Flying Unicorn", "Magical Unicorn")] + [("Llamacorn", "Magical Unicorn")] + [("Extremely Destructive Unicorn", "Magical Unicorn")] + [("Dark Angel Unicorn", "Magical Unicorn")] + [("Classy Narwhal", "Magical Unicorn")] + [("Chainsaw Unicorn", "Magical Unicorn")] + [("Black Knight Unicorn", "Magical Unicorn")] + [("Americorn", "Magical Unicorn")] + [("Alluring Narwhal", "Magical Unicorn")] + [("Unfair Bargain", "Magic Card")] + [("Unicorn Swap", "Magic Card")] + [("Queen Bee Unicorn", "Magical Unicorn")] + [("Stabby the Unicorn", "Magical Unicorn")] + [("Barbed Wire", "Downgrade")] + [("Necromancer Unicorn", "Magical Unicorn")] + [("Rainbow Unicorn", "Magical Unicorn")] + [("Greedy Flying Unicorn", "Magical Unicorn")] + [("Annoying Flying Unicorn", "Magical Unicorn")]
        self.cards = [UnoCard(name_and_typing[0], name_and_typing[1]) for name_and_typing in names_typings]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
    
    def __str__(self):
        return str([str(card) for card in self.cards])


# In[309]:


class UnoGame:
    def __init__(self, players):
        self.deck = UnoDeck()
        self.players = players
        self.current_player = 0
        self.discard = []
        self.limbo = []
        pygame.init()                   # Initialize Pygame
        self.font = pygame.font.Font(r'C:\Users\Keith\New folder\Card Games\OstrichSans-Heavy\OstrichSans-Heavy.otf', 24)
        self.next_time = 0
        self.clock = pygame.time.Clock()
        self.viewing_discard = False
                                        

    def start(self):
        self.deck.shuffle()
        self.deal_initial_cards()
                                        # set up game screen
        width, height = 800, 600
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Click Game")
        
        running = True
        while running:
                                        # If quit
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True
            self.play_turn()
            if self.check_winner():
                break
            self.next_player()
                                        # pygame close
        pygame.quit()
        sys.exit()

    def deal_initial_cards(self):
        for _ in range(7):
            for player in self.players:
                player.hand.append(self.deck.draw_card())
                
    def get_card(self, coords):
        acting_player = self.players[self.current_player]
        mouse_x, mouse_y = coords
        player, loc, card, box = None, None, None, None
                
        user_hand = pygame.Rect(0, self.screen.get_height() - 105, 75 * len(acting_player.hand), 105)
        if user_hand.collidepoint((mouse_x, mouse_y)):
            loc, card, box = acting_player.hand, acting_player.hand[int(mouse_x / 75)], pygame.Rect(75 * int(mouse_x / 75), self.screen.get_height() - 105, 75, 105)
                    
        user_stable = pygame.Rect(0, self.screen.get_height() - 220, 75 * len(acting_player.stable), 105)
        if user_stable.collidepoint((mouse_x, mouse_y)):
            loc, card, box = acting_player.stable, acting_player.stable[int(mouse_x / 75)], pygame.Rect(75 * int(mouse_x / 75), self.screen.get_height() - 210 - 10, 75, 105)
        
        if pygame.Rect(0, self.screen.get_height() - 220, 75 * 7, 220).collidepoint((mouse_x, mouse_y)):
            player = acting_player
                    
        other_players = [each_player for each_player in self.players if each_player != acting_player]
        other_hands = pygame.Rect(0, 0, 75 * 7 + (75 * 7 + 5) * (len(other_players) - 1), 105 * 2)
        if other_hands.collidepoint((mouse_x, mouse_y)):
            player_space = int(mouse_x / (75 * 7 + 5))
            hand_len = len(other_players[player_space].hand)
            other_hand = pygame.Rect((75 * 7 + 5) * player_space, 0, 75 * hand_len, 105)
            if other_hand.collidepoint((mouse_x, mouse_y)):
                card_space = int((mouse_x - (75 * 7 + 5) * player_space) / 75)
                loc, card, box = other_players[player_space].hand, other_players[player_space].hand[card_space], pygame.Rect(75 * card_space + (75 * 7 + 5) * player_space, 0, 75, 105)
            if not card:
                stable_len = len(other_players[player_space].stable)
                other_stable = pygame.Rect((75 * 7 + 5) * player_space, 105, 75 * stable_len, 210)
                if other_stable.collidepoint((mouse_x, mouse_y)):
                    card_space = int((mouse_x - (75 * 7 + 5) * player_space) / 75)
                    loc, card, box = other_players[player_space].stable, other_players[player_space].stable[card_space], pygame.Rect(75 * card_space + (75 * 7 + 5) * player_space , 105, 75, 105)
            player = other_players[player_space]

        return player, loc, card, box

    def display_game_state(self):
        font = self.font
        self.screen.fill((255, 255, 255))
        
        # 30 fps
        self.clock.tick(30)
        
        text = font.render("The deck:" + str([card.name for card in self.deck.cards]), True, (0, 0, 0))
        self.screen.blit(text, (0, 0)) 
        text = font.render("Discard pile:" + str([str(card) for card in self.discard]), True, (0, 0, 0))
        self.screen.blit(text, (0, 20))
        '''
        fps = 1 / (time.time() - self.next_time)
        text = font.render("FPS: " + str(fps), True, (0, 0, 0))
        self.next_time = time.time()
        text_rect = text.get_rect(topright=(self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(text, (725, 525))
        '''

        # Current Player's stable and hand
        i = 0
        for each_card in self.players[self.current_player].hand:
            self.screen.blit(pygame.transform.scale(each_card.image, (75, 105)), (75 * i, self.screen.get_height() - 105))
            i += 1
        i = 0
        for each_card in self.players[self.current_player].stable:
            self.screen.blit(pygame.transform.scale(each_card.image, (75, 105)), (75 * i, self.screen.get_height() - 105 * 2 - 10))
            i += 1
        # Other players' stables and hands
        other_players = [each_player for each_player in self.players if each_player != self.players[self.current_player]]
        for n in range(len(other_players)):
            i = 0
            for each_card in other_players[n].hand:
                self.screen.blit(pygame.transform.scale(each_card.image, (75, 105)), (75 * i + (75 * 7 + 5) * n, 0))
                i += 1
            i = 0
            for each_card in other_players[n].stable:
                self.screen.blit(pygame.transform.scale(each_card.image, (75, 105)), (75 * i + (75 * 7 + 5) * n, 105))
                i += 1
                
        # Discard pile
        mouse_x, mouse_y = pygame.mouse.get_pos()
        discard_pile_height = self.screen.get_height() / 2 - 150
        back = pygame.image.load("Black Back of Card.png")
        self.screen.blit(pygame.transform.scale(back, (75, 105)), (0, discard_pile_height))
        if pygame.Rect(0, discard_pile_height, 75, 105).collidepoint(mouse_x, mouse_y):
            if not self.viewing_discard:
                self.viewing_discard = True
        if self.viewing_discard:
            if not pygame.Rect(0, discard_pile_height + 105 * int((len(self.discard) + 1) / 5), 75 * ((len(self.discard) + 1) % 5), 105).collidepoint(mouse_x, mouse_y) and not pygame.Rect(0, discard_pile_height, 75 * 5, 105 * int((len(self.discard) + 1) / 5)).collidepoint(mouse_x, mouse_y):
                self.viewing_discard = False
        if self.viewing_discard:
            for index, card in enumerate(self.discard):
                self.screen.blit(pygame.transform.scale(card.image, (75, 105)), (75 * ((index + 1) % 5), discard_pile_height + 105 * int((index + 1) / 5)))
    
    def reload_deck(self):
        self.deck.cards += self.discard
        self.deck.shuffle()
        self.discard = []
        
    def play_turn(self):
        player = self.players[self.current_player]
        player.beginning_phase(self)
        for each_player in self.players:
            while len(each_player.hand) > 7:
                each_player.discard(each_player.ask_question(self, "discard down to 7", each_player.hand), self)
        print("=====================")
            
    def is_valid(self, card):
        return True

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def get_next_player(self):
        return self.players[(self.current_player + 1) % len(self.players)]

    def check_winner(self):
        for player in self.players:
            if len([unicorn_card for unicorn_card in player.stable if unicorn_card.typing in ["Magical Unicorn", "Basic", "Baby"]]) >= 7:
                print(f"\n{player} wins!")
                return True
        return False


# In[310]:


class UnoPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stable = [UnoCard("Baby Unicorn", "Baby")]
    
    def beginning_phase(self, game):
        if [card for card in self.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]] and "Sadistic Ritual" in [card.name for card in self.stable] and "Pandamonium" not in [card.name for card in self.stable]:
            self.sacrifice(self.ask_question(game, "pick a Unicorn card to sacrifice", [card for card in self.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]]), game)
            self.draw(game)
        remaining_options = ["Claw Machine", "Caffeine Overload", "Rhinocorn", "Glitter Bomb", "Rainbow Lasso", "Stable Artillery"]
        triggers = [card for card in self.stable if card.name in remaining_options]
        while triggers:
            if self.ask_question(game, "would you like to use a beginning effect?", ["Yes", "No"]) == "Yes":
                if len(triggers) > 1:
                    choice = self.ask_question(game, "which effect", [card.name for card in self.stable if card.name in remaining_options and (card.name != "Rhinocorn" or "Blinding Light" not in [card.name for card in self.stable])])
                else:
                    if "Rhinocorn" in [card.name for card in self.stable] and "Blinding Light" in [card.name for card in self.stable] and "Pandamonium" not in [card.name for card in self.stable]:
                        choice = None
                        break
                    else:
                        choice = triggers[0].name
                remaining_options.remove(choice)
        # Beginning effects go here
                if choice == "Rainbow Lasso" and len(self.hand) >= 3:
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    victim = self.ask_question(game, "pick a Player to steal from", [player for player in game.players if [card for card in player.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]] and "Pandamonium" not in [card.name for card in player.stable]])
                    stolen_unicorn = self.ask_question(game, "pick a Unicorn card to steal", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]])
                    self.steal(stolen_unicorn, victim, game)
                if choice == "Stable Artillery" and len(self.hand) >= 2:
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    self.assign_destroy_unicorn_nomagic(game)
                if choice == "Claw Machine" and len(self.hand) >= 1:
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                    self.draw(game)
                if choice == "Glitter Bomb":
                    self.sacrifice(self.ask_question(game, "pick a card to sacrifice", self.stable), game)
                    self.assign_destroy_nomagic(game)
                if choice == "Caffeine Overload":
                    self.sacrifice(self.ask_question(game, "pick a card to sacrifice", self.stable), game)
                    self.draw(game, 2)
                if choice == "Rhinocorn": # Rhinocorn can probably be selected if no targets exist 
                    self.assign_destroy_unicorn_nomagic(game)
                    print("Rhinocorn ended turn")
                    break
        # End of beginning effects
            else:
                choice = None
                break
            triggers = [card for card in self.stable if card.name in remaining_options]
        else:
            choice = None
            print(self.name, "has nothing to begin with")
        if choice != "Rhinocorn":
            self.draw_phase(game)
    def draw_phase(self, game):
        self.draw(game)
        print(self.name, "drew a card!")
        game.display_game_state()
        if "Double Dutch" in [card.name for card in self.stable]:
            self.action_phase(self.ask_question(game, "pick a card: ", [card for card in self.hand if not (card.typing == "Upgrade" and "Broken Stable" in [card.name for card in self.stable]) and (card.name != "Unicorn Swap" or "Pandamonium" not in [card.name for card in self.stable])]), game)
        self.action_phase(self.ask_question(game, "pick a card: ", [card for card in self.hand if not (card.typing == "Upgrade" and "Broken Stable" in [card.name for card in self.stable]) and (card.name != "Unicorn Swap" or "Pandamonium" not in [card.name for card in self.stable])]), game)
    def action_phase(self, card, game):
        print(self.name, " played ", card)
        self.hand.remove(card)
        queenbee_holder = [player for player in game.players if "Queen Bee Unicorn" in [card.name for card in player.stable] and "Blinding Light" not in [card.name for card in player.stable]]
        if card.typing in ["Magical Unicorn", "Basic", "Baby"]:
            target = self
            if queenbee_holder and card.typing == "Basic":
                target = queenbee_holder[0] # can only sustain 1 Queen Bee or it breaks
            target.stable.append(card)
            target.moved_card(card, game)
    # Unicorn beginning
            if "Blinding Light" not in [card.name for card in self.stable] or "Pandamonium" in [card.name for card in self.stable]:
                if card.name == "Narwhal Torpedo":
                    game.discard += [card for card in self.stable if card.typing == "Downgrade"]
                    [self.sacrifice(card, game) for card in self.stable if card.typing == "Downgrade"]
                if card.name == "Extremely Destructive Unicorn":
                    for each_player in [player for player in game.players if "Pandamonium" not in [card.name for card in player.stable]]:
                        each_player.sacrifice(each_player.ask_question(game, "pick a Unicorn card to sacrifice", [card for card in each_player.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]]), game)
                if card.name == "Llamacorn":
                    for each_player in game.players:
                        each_player.discard(each_player.ask_question(game, "pick a card to discard", each_player.hand), game)
                # All the optional entry effects
                if card.name in ["Dark Angel Unicorn", "Necromancer Unicorn", "Seductive Unicorn", "Annoying Flying Unicorn", "Mother Goose Unicorn", "Rainbow Unicorn", "Alluring Narwhal", "Americorn", "Chainsaw Unicorn", "Mermaid Unicorn", "Magical Flying Unicorn", "Majestic Flying Unicorn", "Greedy Flying Unicorn", "Unicorn Oracle", "Unicorn on the Cob", "Shark With a Horn", "Classy Narwhal", "Shabby the Narwhal", "The Great Narwhal"]:
                    if self.ask_question(game, "would you like to use the secondary effect?", ["Yes", "No"]) == "Yes":
                        if card.name == "Greedy Flying Unicorn":
                            self.draw(game)
                # Oracle probably breaks when less than 3 cards left
                        if card.name == "Unicorn Oracle":
                            [game.limbo.append(game.deck.draw_card()) for n in range(3)]
                            choosen_card = self.ask_question(game, "choose a card", game.limbo)
                            self.hand.append(choosen_card)
                            game.limbo.remove(choosen_card)
                            choosen_card = self.ask_question(game, "which card should be drawn next", game.limbo)
                            game.limbo.remove(choosen_card)
                            game.deck.cards += game.limbo + [choosen_card]
                            game.limbo = []
                        if card.name == "Unicorn on the Cob":
                            self.draw(game, 2)
                            self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                        if card.name == "Shark With a Horn":
                            self.sacrifice(card, game)
                            self.assign_destroy_unicorn_nomagic(game)
                        if card.name == "Classy Narwhal":
                            chosen_card = self.ask_question(game, "Pick an upgrade from the deck", [card for card in game.deck.cards if card.typing == "Upgrade"])
                            if chosen_card:
                                game.deck.cards.remove(chosen_card)
                                self.hand.append(chosen_card)
                                game.deck.shuffle()
                        if card.name == "Shabby the Narwhal":
                            chosen_card = self.ask_question(game, "Pick a downgrade from the deck", [card for card in game.deck.cards if card.typing == "Downgrade"])
                            if chosen_card:
                                game.deck.cards.remove(chosen_card)
                                self.hand.append(chosen_card)
                                game.deck.shuffle()
                        if card.name == "The Great Narwhal":
                            chosen_card = self.ask_question(game, "Pick a narwhal from the deck", [card for card in game.deck.cards if "Narwhal" in card.name])
                            if chosen_card:
                                game.deck.cards.remove(chosen_card)
                                self.hand.append(chosen_card)
                                game.deck.shuffle()
                        if card.name == "Majestic Flying Unicorn":
                            revive = self.ask_question(game, "pick a Unicorn card from the discard", [card for card in game.discard if card.typing in ["Magical Unicorn", "Basic"]])
                            if revive:
                                game.discard.remove(revive)
                                self.hand.append(revive)
                        if card.name == "Magical Flying Unicorn":
                            revive = self.ask_question(game, "Pick a Magic card from the discard", [card for card in game.discard if card.typing == "Magic Card"])
                            if revive:
                                game.discard.remove(revive)
                                self.hand.append(revive)
                        if card.name == "Mermaid Unicorn":
                            victim = self.ask_question(game, "Pick a player to pickup a card", [player for player in game.players if player.stable])
                            victim.return_to_hand(self.ask_question(game, "Pick a card", victim.stable), game)
                        if card.name == "Chainsaw Unicorn":
                            if self.ask_question(game, "choose between", ["Destroy upgrade", "Sacrifice downgrade"]) == "Destroy upgrade":
                                victim = self.ask_question(game, "Pick a player", [player for player in game.players if "Upgrade" in [card.typing for card in player.stable]])
                                if victim:
                                    victim.destroy(self.ask_question(game, "Pick an upgrade to destroy", [card for card in victim.stable if card.typing == "Upgrade"]), game)
                            else:
                                self.sacrifice(self.ask_question(game, "Pick a downgrade", [card for card in self.stable if card.typing == "Downgrade"]), game)
                        if card.name == "Americorn":
                            victim = self.ask_question(game, "pick a player to take a card from", [player for player in game.players if len(player.hand) > 0])
                            random_card = victim.hand[int(random.random() * len(victim.hand))]
                            self.hand.append(random_card)
                            victim.hand.remove(random_card)
                            print(self.name, "stole", random_card, "from", victim.name)
                        if card.name == "Alluring Narwhal":
                            victim = self.ask_question(game, "pick a player to steal an upgrade from", [player for player in game.players if "Upgrade" in [card.typing for card in player.stable]])
                            if victim:
                                self.steal(self.ask_question(game, "pick an upgrade to steal", [upgrades for upgrades in victim.stable if upgrades.typing == "Upgrade"]), victim, game)
                        if card.name == "Rainbow Unicorn":
                            if "Basic Unicorn" in [card.name for card in self.hand]:
                                self.action_phase([card for card in self.hand if card.typing == "Basic"][0], game)
                                print("A Basic followed")
                        if card.name == "Mother Goose Unicorn":
                            self.stable.append(UnoCard("Baby Unicorn", "Baby"))
                            self.moved_card(UnoCard("Baby Unicorn", "Baby"), game)
                        if card.name == "Annoying Flying Unicorn":
                            victim = self.ask_question(game, "pick a player to discard a card", game.players)
                            if victim:
                                victim.discard(victim.ask_question(game, "pick a card to discard", victim.hand), game)
                        if card.name == "Seductive Unicorn":
                            self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                            victim = self.ask_question(game, "pick a Player to steal from", [player for player in game.players if [card for card in player.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]] and "Pandamonium" not in [card.name for card in player.stable]])
                            stolen_unicorn = self.ask_question(game, "pick a Unicorn card to steal", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]])
                            self.steal(stolen_unicorn, victim, game)
                        if card.name == "Necromancer Unicorn":
                            self.discard(self.ask_question(game, "pick a Unicorn card to discard", [card for card in self.hand if card.typing in ["Magical Unicorn", "Basic"]]), game)
                            self.discard(self.ask_question(game, "pick a Unicorn card to discard", [card for card in self.hand if card.typing in ["Magical Unicorn", "Basic"]]), game)
                            revive = self.ask_question(game, "pick a Unicorn card from the discard", [card for card in game.discard if card.typing in ["Magical Unicorn", "Basic"]])
                            if revive:
                                game.discard.remove(revive)
                                self.hand.append(revive)
                                self.action_phase(revive, game)
                        if card.name == "Dark Angel Unicorn" and "Pandamonium" not in [card.name for card in self.stable]:
                            self.sacrifice(self.ask_question(game, "pick a Unicorn card to sacrifice", [card for card in self.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]]), game)
                            revive = self.ask_question(game, "pick a Unicorn card from the discard", [card for card in game.discard if card.typing in ["Magical Unicorn", "Basic"]])
                            if revive:
                                game.discard.remove(revive)
                                self.hand.append(revive)
                                self.action_phase(revive, game)
    # Unicorn ends and Magic begins
        if card.typing == "Magic Card":
            game.discard.append(card)
            if card.name == "Two-For-One":
                chosen_card = self.ask_question(game, "pick a card to sacrifice", self.stable)
                if chosen_card:
                    self.sacrifice(chosen_card, game)
                    self.assign_destroy_magic(game)
                    self.assign_destroy_magic(game)
            if card.name == "Targeted Destruction":
                if self.ask_question(game, "choose between", ["Destroy upgrade", "Sacrifice downgrade"]) == "Destroy upgrade":
                    victim = self.ask_question(game, "Pick a player", [player for player in game.players if "Upgrade" in [card.typing for card in player.stable]])
                    if victim:
                        victim.destroy(self.ask_question(game, "Pick an upgrade to destroy", [card for card in victim.stable if card.typing == "Upgrade"]), game)
                else:
                    self.sacrifice(self.ask_question(game, "Pick a downgrade", [card for card in self.stable if card.typing == "Downgrade"]), game)
            if card.name == "Reset Button":
                for each_player in game.players:
                    for upgrade_downgrade in [card for card in each_player.stable if card.typing in ["Downgrade", "Upgrade"]]:
                        each_player.sacrifice(upgrade_downgrade, game)
                game.reload_deck()
            if card.name == "Shake Up":
                game.discard += self.hand
                self.hand = []
                game.reload_deck()
                self.draw(game, 5)
            if card.name == "Mystical Vortex":
                for each_player in game.players:
                    each_player.discard(each_player.ask_question(game, "pick a card to discard", each_player.hand), game)
                game.reload_deck()
            if card.name == "Re-Target":
                if self.ask_question(game, "choose between", ["Move upgrade", "Move downgrade"]) == "Move upgrade":
                    victim = self.ask_question(game, "Pick a player", [player for player in game.players if "Upgrade" in [card.typing for card in player.stable]])
                    if victim:
                        choose_card = self.ask_question(game, "Pick an upgrade", [card for card in victim.stable if card.typing == "Upgrade"])
                        self.ask_question(game, "Pick someone to give the upgrade to", [player for player in game.players if player != victim]).stable.append(choose_card)
                        victim.stable.remove(choose_card)
                else:
                    victim = self.ask_question(game, "Pick a player", [player for player in game.players if "Downgrade" in [card.typing for card in player.stable]])
                    if victim:
                        choose_card = self.ask_question(game, "Pick a downgrade", [card for card in victim.stable if card.typing == "Downgrade"])
                        self.ask_question(game, "Pick someone to give the downgrade to", [player for player in game.players if player != victim]).stable.append(choose_card)
                        victim.stable.remove(choose_card)
            if card.name == "Kiss of Life":
                revive = self.ask_question(game, "pick a Unicorn card from the discard", [card for card in game.discard if card.typing in ["Magical Unicorn", "Basic"]])
                if revive:
                    game.discard.remove(revive)
                    self.hand.append(revive)
                    self.action_phase(revive, game)
            if card.name == "Good Deal":
                self.draw(game, 3)
                self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
            if card.name == "Change of Luck":
                self.draw(game, 2)
                self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                self.beginning_phase(game)
            if card.name == "Glitter Tornado":
                for victim in game.players:
                    victim.return_to_hand(self.ask_question(game, "Pick a card for " + victim.name + " to pick up", victim.stable), game)
            if card.name == "Blatant Thievery": # Needs to reveal hand
                victim = self.ask_question(game, "pick a Player to steal from", [player for player in game.players if player.hand and player != self])
                chosen_card = self.ask_question(game, "pick a card to take", victim.hand)
                victim.hand.remove(chosen_card)
                self.hand.append(chosen_card)
            if card.name == "Back Kick":
                victim = self.ask_question(game, "Pick a player to pickup a card", [player for player in game.players if player.stable and player != self])
                if victim:
                    victim.return_to_hand(self.ask_question(game, "Pick a card", victim.stable), game)
                    victim.discard(victim.ask_question(game, "pick a card to discard", victim.hand), game)  
            if card.name == "Unfair Bargain":
                victim = self.ask_question(game, "pick a Player to switch hands with", [player for player in game.players if player != self])
                game.limbo, victim.hand = victim.hand, self.hand
                self.hand, game.limbo = game.limbo, []
            if card.name == "Unicorn Poison":
                self.assign_destroy_unicorn_magic(game)
            # Unicorn swap could be cleaned up
            if card.name == "Unicorn Swap": # Will break in 2 player
                if "Queen Bee Unicorn" in [card.name for card in self.stable]:
                    offering = self.ask_question(game, "pick a Unicorn card to give", [card for card in self.stable if card.typing in ["Magical Unicorn", "Baby"]])
                else:
                    offering = self.ask_question(game, "pick a Unicorn card to give", [card for card in self.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"]])
                if queenbee_holder and offering.typing == "Basic":
                    victim = queenbee_holder[0]
                else:
                    victim = self.ask_question(game, "pick a Player to give it to", [player for player in game.players])
                self.give(offering, victim, game)
                if "Queen Bee Unicorn" in [card.name for card in victim.stable]:
                    stolen_unicorn = self.ask_question(game, "pick a Unicorn card to steal", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Baby"] and "Pandamonium" not in [card.name for card in victim.stable]])
                else:
                    stolen_unicorn = self.ask_question(game, "pick a Unicorn card to steal", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"] and "Pandamonium" not in [card.name for card in victim.stable]])
                if stolen_unicorn:
                    self.steal(stolen_unicorn, victim, game)
                
    # Magic ends
        if card.typing == "Upgrade":
            self.stable.append(card)
        if card.typing == "Downgrade":
            self.ask_question(game, "pick a player to give it to", game.players).stable.append(card)

        return card
    def ask_question(self, game, prompt, options):
        light_blue = (0, 127, 255)
        black = (0, 0, 0)
        font = game.font #pygame.font.Font(None, 16)
        if options:
            asking = True
        else:
            asking = False
        out = None
        while asking:
            click_event = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    asking = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_event = True
        
            game.display_game_state()
        
            # The question box
            screen_width, screen_height = game.screen.get_width(), game.screen.get_height()
            box_width, box_height = screen_width // 3, screen_height // 4
    
            rectangle = pygame.Rect(0, 0, box_width, box_height)
            rectangle.center = (screen_width // 2, screen_height // 2)
            pygame.draw.rect(game.screen, light_blue, rectangle)
    
            text = font.render(self.name + ", " + prompt, True, black)
            text_rect = text.get_rect(midtop=(rectangle.centerx, rectangle.top))
            game.screen.blit(text, text_rect)
            
            for n in range(len(options)):
                if str(type(options[n])) == "<class '__main__.UnoCard'>":
                    image_resize = pygame.transform.scale(options[n].image, (50, 70))
                    options_rect = options[n].image.get_rect(center=(rectangle.left + 50 * n + box_width / 2 - len(options) * 50 / 2, rectangle.bottom - 70))
                    game.screen.blit(image_resize, pygame.Rect(rectangle.left + 50 * n + box_width / 2 - len(options) * 50 / 2, rectangle.bottom - 70, 0, 0))
                    #pygame.Rect(100, 200, 200, 150)
                    options_rect = pygame.Rect(rectangle.left + 50 * n + box_width / 2 - len(options) * 50 / 2, rectangle.bottom - 70, 50, 70)
                    #pygame.draw.rect(game.screen, (255, 0, 0), options_rect, width=1)
                    if options_rect.collidepoint(pygame.mouse.get_pos()):
                        game.screen.blit(options[n].image, pygame.Rect(game.screen.get_width() - 400, game.screen.get_height() - 559, 0, 0))
                        pygame.draw.rect(game.screen, (0, 255, 255), options_rect, width=1)
                else:
                    options_text = font.render(str(options[n]), True, black)
                    options_rect = options_text.get_rect(center=(rectangle.left + box_width / (len(options) + 1) * (n + 1), rectangle.centery + n * 12))
                    game.screen.blit(options_text, options_rect)
                    pygame.draw.rect(game.screen, black, options_rect, width=1)
                if click_event and options_rect.collidepoint(pygame.mouse.get_pos()):
                    out = options[n]
                    asking = False
            player, loc, card, box = game.get_card(pygame.mouse.get_pos())
            if card:
                game.screen.blit(card.image, pygame.Rect(game.screen.get_width() - 400, game.screen.get_height() - 559, 0, 0))
                if card in options:
                    pygame.draw.rect(game.screen, (255, 0, 255), box, width=1)
            if click_event:
                if str(type(options[0])) == "<class '__main__.UnoCard'>":
                    if card in options:
                        out = card
                        asking = False
                elif player in options:
                    out = player
                    asking = False
                    
            pygame.display.flip()
        return out 
    def draw(self, game, n=1): # Probably could be reworked
        for i in range(n):
            self.hand.append(game.deck.draw_card())
            if not game.deck.cards:
                print("Shuffled discard pile into the deck!")
                game.reload_deck()
    def move_to(self, card, start, game): # Sacrificed or destroyed, could use cleaning
        if card:
            if "Blinding Light" not in [card.name for card in self.stable]:
                if card.name == "Unicorn Phoenix" and len(self.hand) > 0:
                    self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
                else:
                    self.stable.remove(card)
                    if "Flying" in card.name :
                        self.hand.append(card)
                    elif card.typing != "Baby":
                        game.discard.append(card)
                    if card.typing in ["Magical Unicorn", "Basic", "Baby"]:
                        self.moved_card(card, game)
                    if card.name == "Stabby the Unicorn":
                        self.assign_destroy_unicorn_nomagic(game)
            else:
                self.stable.remove(card)
                if card.typing in ["Magical Unicorn", "Basic", "Baby"]:
                    self.moved_card(card, game)
                if card.typing != "Baby":
                    game.discard.append(card)
    def moved_card(self, card, game):
        if "Barbed Wire" in [downgrade.name for downgrade in self.stable] and card.typing in ["Magical Unicorn", "Basic", "Baby"]:
            self.discard(self.ask_question(game, "pick a card to discard", self.hand), game)
    def give(self, card, victim, game):
        if card:
            print(self.name, "gave", card.name, "to", victim.name)
            self.stable.remove(card)
            self.moved_card(card, game)
            victim.hand.append(card)
            victim.action_phase(card, game)
    def steal(self, card, victim, game):
        if card:
            print(self.name, "stole", card.name, "from", victim.name)
            victim.stable.remove(card)
            victim.moved_card(card, game)
            self.hand.append(card)
            self.action_phase(card, game)
    def discard(self, card, game):
        if card:
            print(self.name, "discarded", card.name)
            game.discard.append(card)
            self.hand.remove(card)
    def return_to_hand(self, card, game):
        if card:
            print(self.name, "picked up", card.name)
            self.stable.remove(card)
            self.moved_card(card, game)
            if card.typing != "Baby":
                self.hand.append(card)
    def assign_destroy_unicorn_nomagic(self, game):
        # Don't forget to adjust the card prompt too
        # Target all cards that are a unicorn and in a stable without Rainbow Aura and Pandamonium, All might break from nesting "card"
        victim = self.ask_question(game, "pick a player", [player for player in game.players if [card for card in player.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"] and "Rainbow Aura" not in [card.name for card in player.stable] and "Pandamonium" not in [card.name for card in player.stable]]])
        if victim:
            victim.destroy(self.ask_question(game, "pick a Unicorn to destroy", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"] and "Rainbow Aura" not in [card.name for card in victim.stable] and "Pandamonium" not in [card.name for card in victim.stable]]), game)
    def assign_destroy_unicorn_magic(self, game):
        # Target all cards that are a unicorn and in a stable without Rainbow Aura and Pandamonium, or are Kittencorn with Blinding Light
        victim = self.ask_question(game, "pick a player", [player for player in game.players if [card for card in player.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"] and "Rainbow Aura" not in [card.name for card in player.stable] and "Pandamonium" not in [card.name for card in player.stable] and (card.name != 'Magical Kittencorn' or "Blinding Light" in [card.name for card in player.stable])]])
        if victim:
            victim.destroy(self.ask_question(game, "pick a card to destroy", [card for card in victim.stable if card.typing in ["Magical Unicorn", "Basic", "Baby"] and "Rainbow Aura" not in [card.name for card in victim.stable] and "Pandamonium" not in [card.name for card in victim.stable] and (card.name != 'Magical Kittencorn' or "Blinding Light" in [card.name for card in victim.stable])]), game)
    def assign_destroy_nomagic(self, game):
        # Target all cards that are not unicorn or not Rainbow Aura in stable or Pandamonium in stable
        victim = self.ask_question(game, "pick a player", [player for player in game.players if [card for card in player.stable if not ("Rainbow Aura" in [card.name for card in player.stable] and card.typing in ["Magical Unicorn", "Basic", "Baby"])]])
        if victim:
            victim.destroy(self.ask_question(game, "pick a card to destroy", [card for card in victim.stable if not ("Rainbow Aura" in [card.name for card in victim.stable] and card.typing in ["Magical Unicorn", "Basic", "Baby"])]), game)
    def assign_destroy_magic(self, game):
        # Cannot target if (!unicorn or !Rainbow Aura) and (!Kittencorn or (Blinding Light and !Pandamonium))
        victim = self.ask_question(game, "pick a player", [player for player in game.players if [card for card in player.stable if (card.typing not in ["Magical Unicorn", "Basic", "Baby"] or "Rainbow Aura" not in [card.name for card in player.stable]) and (card.name != 'Magical Kittencorn' or ("Blinding Light" in [card.name for card in player.stable] and "Pandamonium" not in [card.name for card in player.stable]))]])
        if victim:
            victim.destroy(self.ask_question(game, "pick a card to destroy", [card for card in victim.stable if (card.typing not in ["Magical Unicorn", "Basic", "Baby"] or "Rainbow Aura" not in [card.name for card in victim.stable]) and (card.name != 'Magical Kittencorn' or ("Blinding Light" in [card.name for card in victim.stable] and "Pandamonium" not in [card.name for card in victim.stable]))]), game)
    def destroy(self, card, game):
        if card:
            print(self.name, "destroyed", card.name)
            if card.typing in ["Magical Unicorn", "Basic", "Baby"] and card.name != "Black Knight Unicorn" and "Black Knight Unicorn" in [card.name for card in self.stable] and "Blinding Light" not in [card.name for card in self.stable] and "Pandamonium" not in [card.name for card in self.stable]:
                if self.ask_question(game, "would you like to sacrifice Black Knight Unicorn instead?", ["Yes", "No"]) == "Yes":
                    card = [card for card in self.stable if card.name == "Black Knight Unicorn"][0]
            self.move_to(card, self.stable, game)
    def sacrifice(self, card, game):
        if card:
            print(self.name, "sacrificed", card.name)
            self.move_to(card, self.stable, game)
            
    def __str__(self):
        return self.name


# In[311]:


def main():
    num_players = int(input("Enter the number of players: "))
    #players = [UnoPlayer(input(f"Enter the name of player {i + 1}: ")) for i in range(num_players)]
    players = [UnoPlayer(str(i + 1)) for i in range(num_players)]
    game = UnoGame(players)
    game.start()

if __name__ == "__main__":
    main()


# In[ ]:




