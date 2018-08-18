from enum import Enum

from rlbot.utils.structures.quick_chats import QuickChats


class QuickChat:

    def __init__(self):
        self.me_previous_stats = None
        self.teammates_previous_stats = []
        self.opponents_previous_stats = []
        self.gg = False
        self.agent = None

    def check(self, agent):
        self.agent = agent
        team_stats = [c.stats for c in agent.teammates]
        opponents_stats = [c.stats for c in agent.opponents]

        if self.me_previous_stats is not None:
            if not agent.game_info.is_match_ended:
                # Check own bot
                if agent.me.stats.goals > self.me_previous_stats.goals:
                    self.goal(QuickChatCause.ME)

                    # Check for assist
                    for cur, last in zip(team_stats, self.teammates_previous_stats):
                        if cur.assists > last.assists:
                            self.assist(QuickChatCause.TEAM)
                elif agent.me.stats.own_goals > self.me_previous_stats.own_goals:
                    self.own_goal(QuickChatCause.ME)
                elif agent.me.stats.saves > self.me_previous_stats.saves:
                    self.save(QuickChatCause.ME)
                elif agent.me.stats.demolitions > self.me_previous_stats.demolitions:
                    self.demolition(QuickChatCause.ME)
                else:
                    # Check Team
                    for cur, last in zip(team_stats, self.teammates_previous_stats):
                        if cur.goals > last.goals:
                            self.goal(QuickChatCause.TEAM)
                        elif cur.own_goals > last.own_goals:
                            self.own_goal(QuickChatCause.TEAM)
                        elif cur.saves > last.saves:
                            self.save(QuickChatCause.TEAM)
                        elif cur.demolitions > last.demolitions:
                            self.demolition(QuickChatCause.TEAM)

                        if cur.assists > last.assists:
                            self.assist(QuickChatCause.TEAM)

                    # Check Opponents
                    for cur, last in zip(opponents_stats, self.opponents_previous_stats):
                        if cur.goals > last.goals:
                            self.goal(QuickChatCause.OPPONENT)
                        elif cur.own_goals > last.own_goals:
                            self.own_goal(QuickChatCause.OPPONENT)
                        elif cur.saves > last.saves:
                            self.save(QuickChatCause.OPPONENT)
                        elif cur.demolitions > last.demolitions:
                            self.demolition(QuickChatCause.OPPONENT)
            elif not self.gg:
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.PostGame_Gg)
                agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.PostGame_WellPlayed)
                self.gg = True

        self.me_previous_stats = agent.me.stats.clone()
        self.teammates_previous_stats = [s.clone() for s in team_stats]
        self.opponents_previous_stats = [s.clone() for s in opponents_stats]

    def goal(self, cause):
        if cause == QuickChatCause.ME:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Siiiick)
        elif cause == QuickChatCause.TEAM:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_NiceShot)
        elif cause == QuickChatCause.OPPONENT:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_NiceOne)

    def assist(self, cause):
        if cause == QuickChatCause.TEAM:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_GreatPass)

    def own_goal(self, cause):
        if cause == QuickChatCause.ME:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Apologies_Whoops)
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Apologies_Sorry)
        elif cause == QuickChatCause.TEAM:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Savage)
        elif cause == QuickChatCause.OPPONENT:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Whew)
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_Thanks)

    def save(self, cause):
        if cause == QuickChatCause.ME:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Reactions_Siiiick)
        elif cause == QuickChatCause.TEAM:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_WhatASave)
        elif cause == QuickChatCause.OPPONENT:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Compliments_WhatASave)

    def demolition(self, cause):
        if cause == 1:
            self.agent.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Apologies_Whoops)


class QuickChatCause(Enum):
    ME = 1
    TEAM = 2
    OPPONENT = 3
