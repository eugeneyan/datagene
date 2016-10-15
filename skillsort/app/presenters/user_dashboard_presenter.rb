class UserDashboardPresenter
  
  def initialize(user)
    @user = user
    @game1 = Game.where({user_id: user.id, game_type: 1}).last
    @game2 = Game.where({user_id: user.id, game_type: 2}).last
    @game3 = Game.where({user_id: user.id, game_type: 3}).last
  end


  def game1?
    @game1 || false
  end


  def game2?
    @game2 || false
  end


  def game3?
    @game3 || false
  end


  def love_skills
    @game1 ? @game1.skills_for({game_type: 1, value: 5}) : false
  end


  def like_skills
    @game1 ? @game1.skills_for({game_type: 1, value: 4}) : false
  end


  def neutral_skills
    @game1 ? @game1.skills_for({game_type: 1, value: 3}) : false
  end


  def dislike_skills
    @game1 ? @game1.skills_for({game_type: 1, value: 2}) : false
  end


  def hate_skills
    @game1 ? @game1.skills_for({game_type: 1, value: 1}) : false
  end

end