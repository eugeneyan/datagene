class User < ActiveRecord::Base
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise  :database_authenticatable, :registerable,
          :recoverable, :rememberable, :trackable, :validatable
  validates_presence_of :first_name, :last_name, :email, :birthday_day,
                        :birthday_month, :birthday_year, :gender
  has_many :games

  def has_completed_game? (game_type)
  	self.games.select { |g| g.game_type == game_type }.count > 0
  end

  def has_job_information?
  	self.industry && self.function && self.seniority && self.country
  end

end
