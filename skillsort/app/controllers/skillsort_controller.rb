class SkillsortController < ApplicationController
  include UsersGamesHelper

  before_filter :set_params
  before_filter :game_params, only: :submit_game


  def try_game
  end


  def play_game
    if current_user
      result = check_user_can_attempt_game(current_user, params[:game_type].to_i)
      self.send(result[:action], result[:options])
    else
      self.send('game1', {})
    end
  end


  def game1(options)
    render 'skillsort/game1'
  end


  def game2(options)
    if current_user
      render 'skillsort/game2'			
    else
      redirect_to root_path
    end
  end


  def game3(options)
    if current_user
      if current_user.has_job_information?
        render 'skillsort/game3'
      else
        redirect_to '/job-information'
      end
    else
      redirect_to root_path
    end
  end


  def game_redirect(options)
    @game_title = "Game #{options[:game_type]}"
    @game_title_path = "/play-game/#{options[:game_type]}"
    render 'skillsort/game_redirect'
  end


  def job_information
    redirect_to root_path if !current_user

    @industries = Industry.where({active: true})
    @functions = Function.where({active: true})
    @countries = Country.where({active: true})

  end


  def job_information_submit
    params[:industry] = "Others: " + params[:others_industry] if params[:industry] == "Others"
    params[:function] = "Others: " + params[:others_function] if params[:function] == "Others"
    current_user.update_attributes(params)
    redirect_to '/play-game/3'
  end


  def submit_game
    @game = Game.new(game_params)

    if current_user
      # If player is logged in, then save game
      @game.user_id = current_user.id
      respond_to do |format|
        if @game.save
          format.json { render json: @game, status: 200 }
        else
          format.json { render json: @game.errors, status: :unprocessable_entity }
        end
      end
    else
      render json: {}, status: 200
    end
end


def game_result; end


def dashboard
  @presenter = UserDashboardPresenter.new(current_user)
end


private
# Use callbacks to share common setup or constraints between actions.
def set_game
  @game = Game.find(params[:id])
end

def set_params
  params.permit(:game_type)
end

# Never trust parameters from the scary internet, only allow the white list through.
def game_params
  params.require(:skillsort).permit(:user_id, :version, :result, :game_type)
end

end
