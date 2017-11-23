#init game in rooms.home using self.current_room
#use bool+while loop to check if player is exiting

#
#in home object, define exits: sprites with rects at exit locations
#an exit sprite has a rect, nextroom, nextrect attributes
#rect describes exit sprites location (for checking for player collision)
#- - maybe place these just offscreen for cardinal exits?
#nextroom is the room subclass that we transfer to
#nextrect is the player sprites init rect in the new room
#nextrect cant coincide with any exit rects, so for cardinal exits,
#- - let's place those exits just offscreen ^_^
#
#