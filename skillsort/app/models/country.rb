class Country < ActiveRecord::Base
  scope :active, -> { where( active: true ) }
end