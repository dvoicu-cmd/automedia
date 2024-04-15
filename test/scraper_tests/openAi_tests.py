import pdb

from context import src
from src.scraper.platform_strategies.open_ai_api import OpenAiAPI
from context import lib
from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager



def speech():
    ai = OpenAiAPI()
    ai.text_to_speech("echo", "Man, I remember having sex with a bath bomb in a bath and body works one time. Good shit.")

def image():
    ai = OpenAiAPI()
    ai.stable_diffusion("I want you to generate me an image of a goofy cartoony looney tunes looking ahh nerd with giant glasses reading with intense focus at a comically large book. He also is holding a comically large spoon while smerking at the book.", '/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour')

def text():
    ai = OpenAiAPI()
    res = ai.text_llm("gpt-4", "You are gpt-4-turbo", "Tell me a the story about how you were made.", 80)
    print(res)

def tts():
    ai = OpenAiAPI()
    mg = ScraperDirManager()
    tmp = mg.create_tmp_dir()

    # 400 words
    txt_lordm = """
    
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vehicula, enim et rhoncus malesuada, ante odio feugiat nisl, ac molestie ante est sit amet mi. Nam dignissim rhoncus dui vitae tincidunt. Nam non lobortis orci. Donec in fermentum ipsum. Maecenas sagittis magna a eros laoreet imperdiet. Donec convallis blandit efficitur. Vivamus et rhoncus purus. Pellentesque pellentesque nec erat et eleifend.

Sed et risus consequat, accumsan augue eu, tristique ante. Nulla facilisi. Vivamus ut urna sapien. Vestibulum varius velit sed faucibus auctor. In nulla tellus, vulputate eu elit sed, vestibulum varius nulla. Suspendisse placerat elit orci, eu porta lacus euismod ut. Vestibulum pharetra ex vel lectus porttitor dictum. Donec ut suscipit magna. Sed hendrerit sem ac mattis iaculis. Nullam luctus pulvinar nibh sed blandit. Phasellus rhoncus enim nisi, ut semper risus volutpat eget. Donec venenatis arcu eget magna mollis, id consectetur eros maximus. Phasellus ultrices dui non tellus vehicula vestibulum. Donec interdum arcu volutpat, luctus lectus ac, vestibulum augue.

Donec scelerisque, ante ac malesuada congue, metus leo ultrices neque, vitae interdum risus dui eu elit. Maecenas eget magna ullamcorper, vestibulum turpis dapibus, aliquam nunc. Aenean scelerisque leo at risus auctor, eu mattis diam posuere. Integer scelerisque risus in elementum malesuada. Quisque molestie in nisi a sollicitudin. Nunc congue dolor vel neque rutrum, in suscipit odio pulvinar. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec ac pellentesque est, a tincidunt ligula. Nunc quis libero nunc. Suspendisse quis nibh interdum, scelerisque magna vitae, fringilla enim. Aenean ac dignissim eros. Vestibulum pretium hendrerit nunc, rhoncus dapibus dolor sagittis eget. Morbi convallis justo porttitor tellus feugiat, ut hendrerit magna convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

Donec a ex euismod, faucibus ipsum et, convallis odio. Suspendisse varius bibendum dignissim. Mauris orci nulla, euismod sed scelerisque non, placerat quis nibh. Praesent aliquam, ipsum nec tempor viverra, sem turpis faucibus tellus, ac dictum leo est nec augue. Donec ut tellus lorem. Aenean elementum massa nulla, nec commodo sem pharetra sit amet. Vestibulum in efficitur ex, non vehicula sapien. Proin dignissim justo a nibh tincidunt consectetur. Maecenas scelerisque sodales odio nec ullamcorper. Nam et imperdiet urna. Vivamus ut rhoncus augue. In blandit aliquet enim auctor condimentum. Fusce nec quam tincidunt, vehicula magna et, vestibulum ante. Nam aliquet magna turpis, et pellentesque sem tristique ut. Etiam eleifend odio ligula, ut tempus massa aliquet quis. Etiam vehicula ligula vitae nisl.
    
    """

    four_min_gib = """
    The whimsical flibbertigibbet danced merrily under the moonlight, twirling and spinning in a dizzying display of exuberance. Jellybeans cascaded from the sky, bouncing off umbrellas held by perplexed penguins. Meanwhile, a cacophony of kazoo music filled the air, accompanied by the rhythmic clacking of tap-dancing turtles.

Abracadabra! A swarm of polka-dotted unicorns pranced into view, trailing a rainbow of glitter in their wake. They frolicked through fields of cotton candy clouds, giggling as they chased elusive dreams. Suddenly, a squadron of flying squirrels zoomed past, wearing top hats and monocles, engaged in a high-speed game of chess.

Bippity boppity boo! A chorus of singing snails serenaded a sleepy sloth nestled in a hammock made of licorice. Meanwhile, a mischievous mongoose juggled mangoes while reciting Shakespearean sonnets backwards. And in the distance, a fleet of paper airplanes soared through the sky, carrying messages written in invisible ink.

Zigzagging zephyrs zipped through the zany zoo, tickling the tails of tap-dancing tigers and teasing the toucans with tantalizing treats. Meanwhile, a troupe of tumbling turtles performed acrobatic feats atop towering totem poles, much to the delight of the gathered crowd of gawking giraffes.

Hocus pocus! A whirlwind of wizardry wove its way through the whimsical wonderland, conjuring confetti storms and cotton candy clouds. Meanwhile, a chorus of singing socks serenaded a startled sloth with soulful ballads about the beauty of bedtime.

And as the moon dipped below the horizon, casting its final farewell across the fantastical landscape, the flibbertigibbet paused for a moment of reflection. For in this wondrous world of whimsy and wonder, anything was possible, and every moment was a magical adventure.
    """


    #890 words. This should be about 5 min of text
    ai.text_to_speech("alloy", txt_lordm,tmp)
    pdb.set_trace()
    mg.cleanup(tmp)


def tts_time():
    # 400 words
    txt_lordm = """

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vehicula, enim et rhoncus malesuada, ante odio feugiat nisl, ac molestie ante est sit amet mi. Nam dignissim rhoncus dui vitae tincidunt. Nam non lobortis orci. Donec in fermentum ipsum. Maecenas sagittis magna a eros laoreet imperdiet. Donec convallis blandit efficitur. Vivamus et rhoncus purus. Pellentesque pellentesque nec erat et eleifend.

    Sed et risus consequat, accumsan augue eu, tristique ante. Nulla facilisi. Vivamus ut urna sapien. Vestibulum varius velit sed faucibus auctor. In nulla tellus, vulputate eu elit sed, vestibulum varius nulla. Suspendisse placerat elit orci, eu porta lacus euismod ut. Vestibulum pharetra ex vel lectus porttitor dictum. Donec ut suscipit magna. Sed hendrerit sem ac mattis iaculis. Nullam luctus pulvinar nibh sed blandit. Phasellus rhoncus enim nisi, ut semper risus volutpat eget. Donec venenatis arcu eget magna mollis, id consectetur eros maximus. Phasellus ultrices dui non tellus vehicula vestibulum. Donec interdum arcu volutpat, luctus lectus ac, vestibulum augue.

    Donec scelerisque, ante ac malesuada congue, metus leo ultrices neque, vitae interdum risus dui eu elit. Maecenas eget magna ullamcorper, vestibulum turpis dapibus, aliquam nunc. Aenean scelerisque leo at risus auctor, eu mattis diam posuere. Integer scelerisque risus in elementum malesuada. Quisque molestie in nisi a sollicitudin. Nunc congue dolor vel neque rutrum, in suscipit odio pulvinar. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec ac pellentesque est, a tincidunt ligula. Nunc quis libero nunc. Suspendisse quis nibh interdum, scelerisque magna vitae, fringilla enim. Aenean ac dignissim eros. Vestibulum pretium hendrerit nunc, rhoncus dapibus dolor sagittis eget. Morbi convallis justo porttitor tellus feugiat, ut hendrerit magna convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

    Donec a ex euismod, faucibus ipsum et, convallis odio. Suspendisse varius bibendum dignissim. Mauris orci nulla, euismod sed scelerisque non, placerat quis nibh. Praesent aliquam, ipsum nec tempor viverra, sem turpis faucibus tellus, ac dictum leo est nec augue. Donec ut tellus lorem. Aenean elementum massa nulla, nec commodo sem pharetra sit amet. Vestibulum in efficitur ex, non vehicula sapien. Proin dignissim justo a nibh tincidunt consectetur. Maecenas scelerisque sodales odio nec ullamcorper. Nam et imperdiet urna. Vivamus ut rhoncus augue. In blandit aliquet enim auctor condimentum. Fusce nec quam tincidunt, vehicula magna et, vestibulum ante. Nam aliquet magna turpis, et pellentesque sem tristique ut. Etiam eleifend odio ligula, ut tempus massa aliquet quis. Etiam vehicula ligula vitae nisl.

        """

    est = OpenAiAPI().estimate_tts_time(txt_lordm)
    print(est)


tts_time()
tts()

