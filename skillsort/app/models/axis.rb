class Axis < ActiveRecord::Base
	scope :active, -> { where(active: true) }

	def active?
		self.active
	end
end
