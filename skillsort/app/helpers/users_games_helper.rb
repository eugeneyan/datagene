module UsersGamesHelper

  ##
  # => This method returns a hash with the following actions
  # => {
  # =>   action: 'game1'/'game2'/'game3'/'game_redirect'
  # =>   options: { game_type: 1/2 } (if action is game_redirect)
  # => }

	def check_user_can_attempt_game(user, target_game_type)

    result = {}
  
    if target_game_type == 3
      
      if user.has_completed_game?(1) && user.has_completed_game?(2)
        result[:action] = 'game3'
        result[:options] = {}
      elsif !user.has_completed_game?(1)
        result[:action] = 'game_redirect'
        result[:options] = { game_type: 1 }
      else
        result[:action] = 'game_redirect'
        result[:options] = { game_type: 2 }
      end

    elsif target_game_type == 2

      if user.has_completed_game?(1)
        result[:action] = 'game2'
        result[:options] = {}
      else
        result[:action] = 'game_redirect'
        result[:options] = { game_type: 1 }
      end

    elsif target_game_type == 1

      result[:action] = 'game1'
      result[:options] = {}

    end

    result
	end
end