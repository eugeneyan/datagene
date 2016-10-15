class Feedback < ActiveRecord::Base
	validates_presence_of :qn1, :qn2, :qn3, :qn4, :qn5, :qn6, :qn7
end
