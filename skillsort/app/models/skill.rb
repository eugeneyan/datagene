class Skill < ActiveRecord::Base
  scope :active, -> { where( active: true ) }
end
