"""
Mode Engine - Revolutionary modes for Prabh
Manages Roleplay, Dream Life, and Luci modes
"""

import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime
from src.core.redis_manager import get_redis_manager

logger = logging.getLogger(__name__)


class ModeError(Exception):
    """Base exception for mode-related errors"""
    pass


class ModeAlreadyActiveError(ModeError):
    """Raised when trying to activate a mode that's already active"""
    pass


class InvalidModeError(ModeError):
    """Raised when invalid mode is specified"""
    pass


class StateCorruptionError(ModeError):
    """Raised when mode state is corrupted"""
    pass


class ModeManager:
    """
    Central controller for all revolutionary modes
    Manages activation, switching, and state persistence
    """
    
    VALID_MODES = ["roleplay", "dreamlife", "luci"]
    
    def __init__(self):
        self.redis = get_redis_manager()
    
    def get_current_mode(self, user_id: str) -> Optional[str]:
        """
        Get the currently active mode for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Mode name or None if no mode is active
        """
        try:
            key = f"mode:{user_id}:current"
            mode = self.redis.get(key)
            
            if mode and mode in self.VALID_MODES:
                return mode
            
            return None
        except Exception as e:
            logger.error(f"Error getting current mode for {user_id}: {e}")
            return None
    
    def activate_mode(self, user_id: str, mode: str) -> Dict[str, Any]:
        """
        Activate a mode for a user
        
        Args:
            user_id: Telegram user ID
            mode: Mode to activate (roleplay, dreamlife, luci)
            
        Returns:
            Activation result with status and message
            
        Raises:
            InvalidModeError: If mode is not valid
            ModeAlreadyActiveError: If mode is already active
        """
        try:
            # Validate mode
            if mode not in self.VALID_MODES:
                raise InvalidModeError(f"Invalid mode: {mode}. Valid modes: {self.VALID_MODES}")
            
            # Check if mode is already active
            current_mode = self.get_current_mode(user_id)
            if current_mode == mode:
                raise ModeAlreadyActiveError(f"Mode {mode} is already active")
            
            # Deactivate current mode if any
            if current_mode:
                self.deactivate_mode(user_id)
            
            # Activate new mode
            key = f"mode:{user_id}:current"
            self.redis.set(key, mode)
            
            # Initialize mode state if it doesn't exist
            state_key = f"mode:{user_id}:{mode}:state"
            existing_state = self.redis.get(state_key)
            
            if not existing_state:
                initial_state = {
                    "activated_at": datetime.now().isoformat(),
                    "last_interaction": datetime.now().isoformat(),
                    "is_active": True
                }
                self.redis.set(state_key, initial_state)
            else:
                # Update existing state
                existing_state["is_active"] = True
                existing_state["last_interaction"] = datetime.now().isoformat()
                self.redis.set(state_key, existing_state)
            
            logger.info(f"✅ Activated {mode} mode for user {user_id}")
            
            return {
                "success": True,
                "mode": mode,
                "message": f"{mode.capitalize()} mode activated successfully"
            }
            
        except (InvalidModeError, ModeAlreadyActiveError) as e:
            logger.warning(f"Mode activation failed for {user_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error activating mode for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def deactivate_mode(self, user_id: str) -> bool:
        """
        Deactivate the current mode for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if deactivated successfully, False otherwise
        """
        try:
            current_mode = self.get_current_mode(user_id)
            
            if not current_mode:
                logger.info(f"No active mode to deactivate for user {user_id}")
                return True
            
            # Update mode state to inactive
            state_key = f"mode:{user_id}:{current_mode}:state"
            state = self.redis.get(state_key)
            
            if state:
                state["is_active"] = False
                state["deactivated_at"] = datetime.now().isoformat()
                self.redis.set(state_key, state)
            
            # Remove current mode marker
            key = f"mode:{user_id}:current"
            self.redis.client.delete(key) if self.redis.client else None
            
            logger.info(f"✅ Deactivated {current_mode} mode for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deactivating mode for {user_id}: {e}")
            return False
    
    def get_mode_state(self, user_id: str, mode: str) -> Optional[Dict[str, Any]]:
        """
        Get the state for a specific mode
        
        Args:
            user_id: Telegram user ID
            mode: Mode name
            
        Returns:
            Mode state dictionary or None
            
        Raises:
            InvalidModeError: If mode is not valid
            StateCorruptionError: If state is corrupted
        """
        try:
            if mode not in self.VALID_MODES:
                raise InvalidModeError(f"Invalid mode: {mode}")
            
            state_key = f"mode:{user_id}:{mode}:state"
            state = self.redis.get(state_key)
            
            if state:
                # Validate state structure
                if not isinstance(state, dict):
                    raise StateCorruptionError(f"State for {mode} is corrupted")
                
                return state
            
            return None
            
        except StateCorruptionError as e:
            logger.error(f"State corruption detected for {user_id}/{mode}: {e}")
            # Attempt recovery by resetting state
            self._reset_mode_state(user_id, mode)
            raise
        except Exception as e:
            logger.error(f"Error getting mode state for {user_id}/{mode}: {e}")
            return None
    
    def update_mode_state(self, user_id: str, mode: str, state: Dict[str, Any]) -> bool:
        """
        Update the state for a specific mode
        
        Args:
            user_id: Telegram user ID
            mode: Mode name
            state: New state dictionary
            
        Returns:
            True if updated successfully, False otherwise
            
        Raises:
            InvalidModeError: If mode is not valid
        """
        try:
            if mode not in self.VALID_MODES:
                raise InvalidModeError(f"Invalid mode: {mode}")
            
            # Backup current state before update
            self._backup_state(user_id, mode)
            
            # Update last interaction time
            state["last_interaction"] = datetime.now().isoformat()
            
            # Save new state
            state_key = f"mode:{user_id}:{mode}:state"
            success = self.redis.set(state_key, state)
            
            if success:
                logger.info(f"✅ Updated {mode} state for user {user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating mode state for {user_id}/{mode}: {e}")
            return False
    
    def switch_mode(self, user_id: str, new_mode: str) -> Dict[str, Any]:
        """
        Switch from current mode to a new mode
        Preserves state of both modes
        
        Args:
            user_id: Telegram user ID
            new_mode: Mode to switch to
            
        Returns:
            Switch result with status and message
        """
        try:
            current_mode = self.get_current_mode(user_id)
            
            if current_mode == new_mode:
                return {
                    "success": False,
                    "message": f"Already in {new_mode} mode"
                }
            
            # Deactivate current mode (preserves state)
            if current_mode:
                self.deactivate_mode(user_id)
            
            # Activate new mode
            result = self.activate_mode(user_id, new_mode)
            
            if result.get("success"):
                logger.info(f"✅ Switched from {current_mode} to {new_mode} for user {user_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error switching mode for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _backup_state(self, user_id: str, mode: str):
        """Backup current state before major changes"""
        try:
            state_key = f"mode:{user_id}:{mode}:state"
            backup_key = f"mode:{user_id}:{mode}:state:backup"
            
            current_state = self.redis.get(state_key)
            if current_state:
                self.redis.set(backup_key, current_state, expire=3600)  # 1 hour backup
                
        except Exception as e:
            logger.error(f"Error backing up state for {user_id}/{mode}: {e}")
    
    def _reset_mode_state(self, user_id: str, mode: str):
        """Reset mode state to initial state"""
        try:
            state_key = f"mode:{user_id}:{mode}:state"
            initial_state = {
                "activated_at": datetime.now().isoformat(),
                "last_interaction": datetime.now().isoformat(),
                "is_active": False,
                "reset": True
            }
            self.redis.set(state_key, initial_state)
            logger.info(f"Reset state for {user_id}/{mode}")
            
        except Exception as e:
            logger.error(f"Error resetting state for {user_id}/{mode}: {e}")
    
    def recover_state(self, user_id: str, mode: str) -> bool:
        """
        Recover state from backup
        
        Args:
            user_id: Telegram user ID
            mode: Mode name
            
        Returns:
            True if recovered successfully, False otherwise
        """
        try:
            backup_key = f"mode:{user_id}:{mode}:state:backup"
            backup_state = self.redis.get(backup_key)
            
            if backup_state:
                state_key = f"mode:{user_id}:{mode}:state"
                self.redis.set(state_key, backup_state)
                logger.info(f"✅ Recovered state from backup for {user_id}/{mode}")
                return True
            
            logger.warning(f"No backup found for {user_id}/{mode}")
            return False
            
        except Exception as e:
            logger.error(f"Error recovering state for {user_id}/{mode}: {e}")
            return False


# Global instance
_mode_manager = None


def get_mode_manager() -> ModeManager:
    """Get global mode manager instance"""
    global _mode_manager
    if _mode_manager is None:
        _mode_manager = ModeManager()
    return _mode_manager
