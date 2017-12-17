#%%
#   Assume screen width?
#
#
import numpy as np
import cmd

class World():

    star_ratio = 0
    star_locations = []
    state = 0
    ship = 0
    turn = 0


    def __init__(self):
        '''What happens at world startup: World is created, ship is created'''
        self.star_ratio = 0.05
        self.state = np.random.choice(2, (11,11), p=[1 - self.star_ratio, self.star_ratio])
        self.state[5][5] = 1
        self.star_locations = [list(a) for a in zip(np.where(self.state == 1)[0], np.where(self.state == 1)[1])]

        self.ship = Terra0()
        self.check_world_events()
        pass

    def show(self):
        '''
        * : Stars
        T : Terra0
        . : Empty space
        '''
        rl = []
        for row in self.state:
            il = []
            for value in row:
                if value == 1:
                    il.append('*')
                elif value == 9:
                    il.append('T')
                else:
                    il.append('.')
            rl.append(il)

        rl[self.ship.world_location[0]][self.ship.world_location[1]] = 'T'

        # Printout
        print('\n\n\n---------------------')
        print('-       Terra0    -')
        print('---------------------\n')
        for row in rl:
            print('   ' + ''.join(row))
        print('\n\n---------------------')
        print('-      Turn : {}   -'.format(self.turn))
        print('-      Head : {}   -'.format(self.ship.world_heading))
        print('-      Loc  : {}   -'.format(self.ship.world_location))
        print('---------------------')
        print('-      Events      ')


    def end_turn(self):
        '''What happens every turn? Move ships, random events'''

        self.check_world_events()
        self.ship.world_step()
        self.turn = self.turn + 1

    def check_world_events(self):

        # Check if near star
        for location in self.star_locations:
            if location[0] == self.ship.world_location[0]:
                if location[1] == self.ship.world_location[1]:
                    self.trigger_event('star')
                    self.ship.can_trade = True
                else:
                    self.ship.can_trade = False

    def trigger_event(self, event_type):
        if event_type == 'star':
            print('Near Star System')
        if event_type == 'random':
            self.ship.trigger_random_world_event()

class Space():
    '''Class for empty space'''

    is_star = 0

class System():
    '''Star system has planets and stations - for now just trade with system'''
    is_star = 1
    stuffs = ['Apples', 'Oranges', 'Fish', 'Gold', 'Computers', 'Water', 'Steel']
    n_planets = 3
    trade_wares = np.random.choice(stuffs, n_planets)
    trade_prices = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], n_planets)


    def __init__(self):
        pass


class Terra0():
    '''Main class for ship'''
    world_location = [5, 5]
    world_heading = 'stop'
    area_location = [5, 5]
    can_trade = False

    def __init__(self):
        pass

    def world_step(self):

        if self.world_heading == 'left':
            self.world_location[1] = self.world_location[1] - 1
        elif self.world_heading == 'right':
            self.world_location[1] = self.world_location[1] + 1
        elif self.world_heading == 'up':
            self.world_location[0] = self.world_location[0] - 1
        elif self.world_heading == 'down':
            self.world_location[0] = self.world_location[0] + 1
        elif self.world_heading == 'stop':
            pass
        else:
            print('Heading ERROR')

    def set_heading(self, heading):
        self.world_heading = heading

    def trigger_random_world_event(self):
        print('Something went wrong!')
        self.take_damage(1)

    def take_damage(self, amount):
        print("Took damage")



class WorldShell(cmd.Cmd):
    intro = 'Welcome to the Terra0.   Type help or ? to list commands.\n'
    prompt = '[Input]: '
    world = World()
    world.show()


    def do_e(self, arg):
        '''Ends the current turn'''
        self.world.end_turn()
        self.world.show()

    def do_sh(self, heading):
        self.world.ship.set_heading(heading)

    def do_s(self, arg):
        '''Stars'''
        print(self.world.star_locations)

    def do_d(self, arg):
        '''DEBUG FUNCTION'''
#        self.world.trigger_event('random')
        self.world.ship.can_trade = False

    def do_t(self, arg):
        '''Trade'''
        if self.world.ship.can_trade == True:
            print('Can trade')
        else:
            print('Trade not possible')

    def do_test(self, arg):
        print('test')

    def do_q(self, arg):
        '''Ends the game'''
        print('Thank you for playing')

        return True


# Main Loop
if __name__ == '__main__':
    WorldShell().cmdloop()

