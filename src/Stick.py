import pygame
from gameobjects.vector2 import Vector2
from TextDisplay import TextDisplay

class Stick:
	DIRECTION_LEFT = 0
	DIRECTION_RIGHT = 1
	DIRECTION_UP = 2
	DIRECTION_DOWN = 3

	STAND_STATE = 0
	WALK_STATE = 1
	RUN_STATE = 2
	JUMP_STATE = 3

	GRAVITY = 10


	def __init__(self, name, surface):
		self.url_folder = "/home/testme/Pictures/stick2"
		self.image_percentage_size = 0.5
		self.count_image = 0
		self.current_image = None
		self.stick_position = Vector2(0, 0)
		self.stick_direction = Vector2(0, 0)
		self.name = name
		self.surface = surface
		self.speed_game = 250
		self.step_distance = 1
		self.flip = 0
		self.action_state = Stick.STAND_STATE

		self.init_walk()
		self.init_run()
		self.init_jump()

		self.wala = 1000


	def init_walk(self):
		self.stick_walk_images = []
		#self.speed_walk = 250
		self.walk_max_image = 61


		self.load_images('walk2', 'walking2',self.walk_max_image)

	def init_run(self):
		self.stick_run_images = []
		self.run_max_image = 31

		self.load_images('run2', 'Running',self.run_max_image)


	def init_jump(self):
		self.stick_jump_images = []
		self.jump_max = 250
		self.jump_posY_temp = 0
		self.jump_velocity = 0
		self.jump_lock = True
		self.jump_max_image = 61
		self.jump_range = 50

		self.load_images('jump2', 'jumping2',self.jump_max_image)



	def load_images(self, name, file_name,num_of_images):
		for i in range(num_of_images):
			image = pygame.image.load(self.url_folder + "/" + name + "/" + file_name + "." + '{:04d}'.format(i) + ".png")
			if name == "walk" or name == "walk2":
				self.stick_walk_images.append(image)
			elif name == "run2":
				self.stick_run_images.append(image)
			elif name == "jump" or name == 'jump2':
				self.stick_jump_images.append(image)

	def default_stand(self):
		if self.jump_lock:
			self.action_state = Stick.STAND_STATE
			self.count_image = 0


	def walk(self):
		if self.jump_lock:
			self.count_image += 1
			self.count_image = self.count_image % (self.walk_max_image)
			self.action_state = Stick.WALK_STATE
			self.step_distance = 1

	def run(self):
		if self.jump_lock:
			self.count_image += 1
			self.count_image = self.count_image % (self.run_max_image)
			self.action_state = Stick.RUN_STATE
			self.step_distance = 3
		


	def direction(self, position_state):
		if(position_state == Stick.DIRECTION_LEFT):
			self.stick_direction.x = -self.step_distance
			self.flip = 1
		elif(position_state == Stick.DIRECTION_RIGHT):
			self.stick_direction.x = +self.step_distance
			self.flip = 0
		elif(position_state == Stick.DIRECTION_UP):
			self.stick_direction.y = -self.step_distance
		elif(position_state == Stick.DIRECTION_DOWN):
			self.stick_direction.y = +self.step_distance
		else:
			raise NameError("Not supported!")



	def jump(self):
		self.action_state = Stick.JUMP_STATE
		self.__jump_unlock()

	def __jump_unlock(self):
		if self.jump_lock:
			self.jump_lock = False
			self.jump_distance = 15
			self.jump_posY_temp = self.stick_position.y
			self.count_image = 50
			self.jump_velocity = 0
			self.velocity_speed = 0.2

	def __jump_lock(self):
		self.action_state = Stick.STAND_STATE
		self.jump_lock = True
		self.step_distance = 1

	def do_action(self, seconds):

		'''if self.jump_lock:
			self.current_image = self.stick_walk_images[self.count_image]
		else:

			if self.__check_jump_done(seconds):
				self.__jump_lock()
			self.current_image = self.stick_jump_images[self.count_image]'''

		if self.action_state == Stick.WALK_STATE:
			self.current_image = self.stick_walk_images[self.count_image]
		elif self.action_state == Stick.JUMP_STATE:
			if self.__check_jump_done(seconds):
				self.__jump_lock()
			self.current_image = self.stick_jump_images[self.count_image]
		elif self.action_state == Stick.RUN_STATE:
			self.current_image = self.stick_run_images[self.count_image]
		else:
			self.current_image = self.stick_walk_images[0]
		


		self.stick_position += self.stick_direction * seconds * self.speed_game
		self.stick_direction = Vector2(0, 0)
		
	def __check_jump_done(self, seconds):
		if self.__jump_animate_done():
				if self.stick_position.y > self.jump_posY_temp + 2:
					self.stick_position.y = self.jump_posY_temp
					return True

				self.test_jump()

				self.stick_direction.y = -(self.jump_distance * self.velocity_speed) + self.jump_velocity
				self.jump_velocity += self.velocity_speed
		else:
			self.stick_direction.x = 0

	def test_jump(self):
		if self.wala > self.stick_position.y:
			self.wala = self.stick_position.y

	def __jump_animate_done(self):
		if self.count_image < self.jump_max_image - 1:
			self.count_image += 1
		else:
			return True

	def render(self):
		if self.current_image != None:
			image = self.current_image
			image = pygame.transform.scale(image, (int(image.get_width() * self.image_percentage_size), int(image.get_height() * self.image_percentage_size)))
			image = pygame.transform.flip(image, self.flip, 0)
			self.surface.blit(image, (self.stick_position.x, self.stick_position.y))

	def display_test(self):
		TextDisplay.printline("==============================================")
		TextDisplay.printline("Name: " + self.name)
		TextDisplay.printline("Position: " + str(self.stick_position))
		strState = { 
			0 : "STAND",
			1 : "WALK",
			2 : "RUN",
			3 : "JUMP"}
		TextDisplay.printline("Action state: " + strState[self.action_state])
		TextDisplay.printline("==============================================")

if __name__ == "__main__":
	from pygame.locals import *

	pygame.init()

	screen = pygame.display.set_mode((640, 480), 0 , 32)
	background = pygame.Surface((screen.get_size()))
	background.fill((255,255,255))
	background = background.convert()

	font = pygame.font.SysFont("arial", 16)

	TextDisplay.init(screen, font,(0,0,255))

	stick1 = Stick("Stick1",screen)
	stick2 = Stick("Stick2",screen)

	clock = pygame.time.Clock()
	FPS = 60
	interval = .0
	cycletime = 0


	while True:
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				pygame.quit()
				from sys import exit
				exit()

		screen.blit(background, (0, 0))


		milli = clock.tick(FPS)
		TextDisplay.printline("Current milliseconds: " + str(milli))
		seconds = milli / 1000.0
		cycletime += seconds


		pressed_keys = pygame.key.get_pressed()

		if cycletime > interval:
			cycletime = 0
			isKeyRelease = True


			#Stick # 1---------------------------------------------------------------------------

			if pressed_keys[K_a]:
				stick1.direction(Stick.DIRECTION_LEFT)
				isKeyRelease = False
			if pressed_keys[K_d]:
				stick1.direction(Stick.DIRECTION_RIGHT)
				isKeyRelease = False
			if pressed_keys[K_w]:
				stick1.direction(Stick.DIRECTION_UP)
				isKeyRelease = False
			if pressed_keys[K_s]:
				stick1.direction(Stick.DIRECTION_DOWN)
				isKeyRelease = False

			if pressed_keys[K_SPACE]:
				stick1.jump()


			if isKeyRelease:
				stick1.default_stand()
			else:
				if pressed_keys[K_LSHIFT]:
					stick1.run()
				else:
					stick1.walk()

			stick1.do_action(seconds)



			#Stick # 2---------------------------------------------------------------------------


			

			stick2.do_action(seconds)


		stick1.render()
		stick1.display_test()

		stick2.render()
		stick2.display_test()

		TextDisplay.display()
		pygame.display.update()










	
	