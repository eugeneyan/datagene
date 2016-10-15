class Industry < ActiveRecord::Base
	scope :active, -> { where(active: true) }
end
