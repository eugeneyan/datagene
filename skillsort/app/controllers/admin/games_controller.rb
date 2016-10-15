module Admin
  class GamesController < Admin::AdminController
    before_action :set_game, only: [:show, :edit, :update, :destroy]


    # GET /games
    # GET /games.json
    def index
      @games = Game.all
    end


    # GET /games/1
    # GET /games/1.json
    def show; end


    # Sends a CSV formated report of a game to client
    def download
      Game.find(params[:id]).populateResult!
      @filename = Rails.public_path.to_s+'/game_result.csv'
      send_file(@filename, :filename => "game_result.csv")
    end


    # Sends a CSV formated report of all games to client
    def download_all
      Game.allResults!
      @filename = Rails.public_path.to_s+'/game_all_results.csv'
      send_file(@filename, :filename => "game_all_results.csv")
    end


    # GET /games/new
    def new
      @game = Game.new
    end


    # GET /games/1/edit
    def edit; end


    # POST /games
    # POST /games.json
    def create
      @game = Game.new(game_params)

      respond_to do |format|
        if @game.save
          format.html { redirect_to @game, notice: 'Game was successfully created.' }
          format.json { render action: 'show', status: :created, location: @game }
        else
          format.html { render action: 'new' }
          format.json { render json: @game.errors, status: :unprocessable_entity }
        end
      end
    end


    # PATCH/PUT /games/1
    # PATCH/PUT /games/1.json
    def update
      respond_to do |format|
        if @game.update(game_params)
          format.html { redirect_to @game, notice: 'Game was successfully updated.' }
          format.json { head :no_content }
        else
          format.html { render action: 'edit' }
          format.json { render json: @game.errors, status: :unprocessable_entity }
        end
      end
    end


    # DELETE /games/1
    # DELETE /games/1.json
    def destroy
      @game.destroy
      respond_to do |format|
        format.html { redirect_to admin_games_url }
        format.json { head :no_content }
      end
    end


    private


    # Use callbacks to share common setup or constraints between actions.
    def set_game
      @game = Game.find(params[:id])
    end


    # Only allow the white list through.
    def game_params
      params.require(:game).permit(:user_id, :version, :game_type, :result)
    end
  end
end